---
title: 敏捷开发-Agile 
author: Teddy
date: 2020-09-22 20:05:23 +0800
categories: [实践, 敏捷开发]
tags: [Agile]
---

# 敏捷开发

## 敏捷团队中的角色

**Business owner**

* 行业客户，需求提出方

**Developer**

* 开发工程师，开发需求并交付产品

**End user**

* 端用户，产品面向用户

**BA**

* *Business Analyst* - 业务分析员
* 负责理解并挖掘客户的需求，然后将需求转化为具体的 *AC*（*Acceptance criteria*, 验收标准）
* 作为 *Business owner* 和 *Developer* 直接的桥梁，将业务知识最大化的传递给 *Developer* ，保证工程师对业务准确的理解

**QA**

* *Quality Analyst* - 质量分析师
* *Quality Assurance* - 质量保证
* *tester* 的职责是按照 *AC* ，对系统功能进行测试，包括功能性、安全性、性能等维度保证系统的健壮性及所开发功能符合 *AC*
* *QA* 的职责不仅仅只是一个 *tester*， *QA* 的职责不是单纯的在开发完成后，接收 *AC* 并测试。为了解决开发过程中参与度不足导致的需求衰减问题，*QA* 应尽早接入用户故事的前期工作，在BA分析 *user story* 及细分任务时就应该准备开发环境、测试策略、测试数据。
* tester可以从测试的角度给开发人员提供一些建议。而在开发人员开发卡的时候，tester可以和开发人员一起pair编写自动化的测试用例。开发人员开发完毕后，tester可以在开发人员的本地环境中快速验证其是否满足所有验收条件，必要的自动化测试是否已经完成等。在UAT环节，tester又可以帮助business owner进行sign off
* *QA* 作为连接器把需求过程中的每个环节的参与者串联起来，他的职责已经超出了开发所理解的单纯的 *tester*，所以将这个角色定义为**质量分析师**，在整个产品的生命周期中保证产品的质量，最终高质量交付

## 敏捷开发中的重要概念

* TODO