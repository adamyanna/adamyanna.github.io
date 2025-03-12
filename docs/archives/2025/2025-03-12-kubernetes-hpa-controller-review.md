---
title: Kubernetes HPA Controller [Reivew]
layout: default
parent: 2025
grand_parent: Archives
---

**Kubernetes**
{: .label .label-blue }

**HPA**
{: .label .label-blue }

# Kubernetes HPA Controller Horizontal Scaling Key Implementations

## Table of Contents

1. Introduction
   - 1.1 Horizontal Scaling Mechanism
   - 1.2 Four HPA Ranges
   - 1.3 Metric Types
   - 1.4 Delay Queue
   - 1.5 Monitoring Time Series Window
   - 1.6 Stability and Delay
2. Core Implementation
   - 2.1 Fetching Scale via ScaleTargetRef
   - 2.2 Interval Decision
   - 2.3 Core Logic of HPA Dynamic Scaling Decision
   - 2.4 Multi-Dimensional Metric Replica Count Decision
   - 2.5 Pod Metric Calculation and Desired Replica Count
   - 2.6 Stability Decision with Behavior
3. Advanced Design and Implementation Details
   - 3.1 HPA Algorithm and Calculation Strategy
   - 3.2 Scale-up and Scale-down Strategies
   - 3.3 Handling Multiple Metrics in HPA
   - 3.4 Preventing Thrashing with Stability Windows
   - 3.5 Custom Metrics and External Metrics
4. Implementation Summary

## 1. Introduction

![](/assets/images/docs/kubernetes_kube_hpa.svg)

### 🎯 HPA Workflow

1. Run GoRoutine single worker every 15s to request metrics, Update time period by modify `--horizontal-pod-autoscaler-sync-period`

2. Use **Last 1 min metrics**, to Update **readyPodCount, ignoredPods, missingPods**

   1. TargetUtilization to Update **Last 1 min metrics**
   2. Calcaulate `UsageRatio = CurrentMetricValue / TargetMetricValue`

3. `MetricDesiredReplicas = CurrentReplicas * UsageRatio`

4.  is **UsageRatio**

   1. Greater than 1 -> Scale Up
   2. Smaller than 1 -> Scale Down

5. Base on `MetricDesiredReplicas & MaxReplicas` to get `DesiredReplicas`

   > `computeReplicasForMetrics`

6. Compute `scaleDelaySeconds` from `Behavior.StabilizationWindowSeconds`

7. Compute `betterRecommendation` as final Replicas to be deployed 

8. Behavior

   * `calculateScaleUpLimitWithScalingRules`
   * `calculateScaleDownLimitWithBehaviors`

9. `newReplicas` - `curReplicas` get current window Pod Count for either UP or Down

#### 🎯 Key Steps

* **Delay Queue**
  * Run go routine every 15s to requests metrics & put current HPA resource back to queue for next run
* **Last 5 min** & **Last 1 min**
  * HPA controller will request last **5** min metrics, get the last 1 min metrics for **Replicas** Compute
* **StabilizationWindowSeconds** as **scaleDelay**
  * Keep previous **Recommendation**, avoid rapid scale up & down, make smallest change for Cluster Stabilization

#### 🎯 Example Source Code

```go
// HPA GoRoutine
func (a *HorizontalController) Run(stopCh <-chan struct{}) {
    // ...
    // start a single worker (we may wish to start more in the future)
    go wait.Until(a.worker, time.Second, stopCh)

    <-stopCh
}


```

#### 🎯 APIs

* ```
  /apis/metrics.k8s.io
  /apis/custom.metrics.k8s.io
  /apis/external.metrics.k8s.io
  ```

* ```javascript
  /api/v1/model/namespaces/{namespace}/pod-list/{podName1,podName2}/metrics/{metricName}
  ```

* ```
  http://<node-ip>:4194/metrics
  http://<node-ip>:10255/stats/summary
  ```

### 1.1 Horizontal Scaling Mechanism

The HPA controller implementation mainly retrieves the current HPA object via an informer, then fetches the monitoring data of the corresponding Pod set via the metrics service. Based on the current target object's scale status, the expansion algorithm determines the number of replicas and updates the Scale object to achieve automatic scaling. 

The primary components involved in HPA include:
- **HPA Controller**: Watches resource utilization and adjusts replicas accordingly.
- **Metrics Server**: Collects and exposes resource metrics like CPU and memory usage.
- **API Server**: Provides API endpoints for querying HPA status and configuration.
- **Scaling Target (Deployment, StatefulSet, ReplicaSet, etc.)**: The workload managed by HPA.

### 1.2 Four HPA Ranges

HPA divides scaling into four main states based on parameters and current Scale object replica count:
- **Shutdown**: No scaling operations occur.
- **High-Water Mark**: The load is too high, triggering scale-up.
- **Low-Water Mark**: The load is too low, triggering scale-down.
- **Normal**: No scaling required, maintaining stability.

Only when in the normal range will the HPA controller dynamically adjust.

### 1.3 Metric Types

Currently, HPA supports three primary metric types:
- **Resource Metrics**: CPU and Memory utilization.
- **Pod Metrics**: Custom application-level metrics collected from individual Pods.
- **External Metrics**: Metrics from external sources such as Prometheus, Datadog, or CloudWatch.

### 1.4 Delay Queue

The HPA controller does not monitor resource changes in informers like Pod, Deployment, or ReplicaSet. Instead, after processing, the current HPA object is re-added to a delay queue, triggering the next check. The default check interval is **15 seconds**.

### 1.5 Monitoring Time Series Window

When fetching pod monitoring data from the metrics server, the HPA controller retrieves the last **5 minutes of data** and then extracts the **latest 1-minute** data for calculations. This ensures short-term fluctuations do not cause frequent scaling operations.

### 1.6 Stability and Delay

To prevent excessive scaling actions, HPA introduces stability windows:
- **Scale-up stability window**: **3 minutes** before adding replicas.
- **Scale-down stability window**: **5 minutes** before removing replicas.

These windows ensure that scaling operations happen smoothly without excessive fluctuations.

## 2. Core Implementation

### 2.1 Fetching Scale via ScaleTargetRef

HPA retrieves the corresponding resource version via the scheme and then fetches the Scale object through the version information.

```go
// Extracting ScaleTargetRef information
targetGV, err := schema.ParseGroupVersion(hpa.Spec.ScaleTargetRef.APIVersion)
targetGK := schema.GroupKind{
  Group: targetGV.Group,
  Kind: hpa.Spec.ScaleTargetRef.Kind,
}
scale, targetGR, err := a.scaleForResourceMappings(hpa.Namespace, hpa.Spec.ScaleTargetRef)
```

### 2.2 Interval Decision

HPA first determines the current replica count based on the Scale object and configuration parameters. If the count exceeds `maxReplicas` or falls below `minReplicas`, it is simply adjusted to the respective threshold. If replicas are `0`, no action is taken.

```go
if scale.Spec.Replicas == 0 && minReplicas != 0 {
  desiredReplicas = 0
  rescale = false
} else if currentReplicas > hpa.Spec.MaxReplicas {
  desiredReplicas = hpa.Spec.MaxReplicas
}
```

### 2.3 Core Logic of HPA Dynamic Scaling Decision

HPA follows two key steps for scaling decisions:
1. **Determine desired replica count** based on monitoring data.
2. **Adjust final count** using behavior settings to prevent rapid fluctuations.

### 2.4 Multi-Dimensional Metric Replica Count Decision

HPA selects the **maximum replica count proposal** among multiple metric sources to satisfy all scaling requirements.

```go
for i, metricSpec := range metricSpecs {
    replicaCountProposal, _, _, _, err := a.computeReplicasForMetrics(hpa, scale, hpa.Spec)
    if err == nil && (replicas == 0 || replicaCountProposal > replicas) {
        replicas = replicaCountProposal
    }
}
```

### 2.5 Pod Metric Calculation and Desired Replica Count

HPA classifies Pods into three categories when fetching monitoring data:
- **Pending Pods**: Ignored as their status is uncertain.
- **Ready Pods**: Used for metric calculations.
- **Missing Pods**: Either disconnected or failed, handled based on usage ratio.

### 2.6 Stability Decision with Behavior

HPA introduces **expansion (3 min) and shrinkage (5 min) windows** to maintain stability. Scaling is determined based on the smallest value within the window for expansion and the largest value for shrinkage.

```go
if args.DesiredReplicas >= args.CurrentReplicas {
    scaleDelaySeconds = *args.ScaleUpBehavior.StabilizationWindowSeconds
} else {
    scaleDelaySeconds = *args.ScaleDownBehavior.StabilizationWindowSeconds
}
```

## 3. Advanced Design and Implementation Details

### 3.1 HPA Algorithm and Calculation Strategy
- HPA uses a **proportional scaling algorithm**: `(Current Usage / Target Usage) * Current Replicas`
- It ensures that scaling decisions consider both **short-term fluctuations** and **long-term trends**.

### 3.2 Scale-up and Scale-down Strategies
- **Scale-up**: HPA prevents excessive replica additions by capping increases.
- **Scale-down**: Prevents aggressive removal of replicas to avoid instability.

### 3.3 Handling Multiple Metrics in HPA
- HPA supports multiple metrics per deployment.
- Uses **maximum suggested replica count** from all metrics.

### 3.4 Preventing Thrashing with Stability Windows
- Uses past decisions to avoid rapid oscillations.

### 3.5 Custom Metrics and External Metrics
- **Prometheus adapter** allows custom metric integration.

## 4. Implementation Summary

HPA is a **robust, scalable solution** with stability controls. Learning from its **proportional scaling, stability windows, and multi-metric support** can improve autoscaling solutions.

For further reading, refer to:
- [Kubernetes HPA Documentation](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [Prometheus Metrics Adapter](https://github.com/kubernetes-sigs/custom-metrics-apiserver)

