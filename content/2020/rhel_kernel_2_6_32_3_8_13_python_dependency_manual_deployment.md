# RHEL Kernel 2.6.32 / 3.8.13: Python Dependency Manual Deployment

> 2020-05-14

Step-by-step runbook for deploying Python 2.7.5 with pip, setuptools, supervisor, and offline pip packages on legacy Red Hat Enterprise Linux (kernel 2.6.32 / 3.8.13).

## Procedure

### 0. Download Packages from Test Environment

Copy offline packages from `/opt/netmon/pip_pkg` — all dependencies must be available locally (no network access during deployment).

### 1. Install Required System Packages

```bash
yum install -y gcc
yum install -y supervisor
yum install -y libpng-devel
yum install -y python-devel.x86_64
yum install MySQL-python
yum install libffi
yum install libffi-dev
yum install -y openssl-devel
rpm -ivh libffi-devel-3.0.5-3.2.el6.x86_64.rpm

```

### 2. Upgrade Python to 2.7.5

```bash
tar -zxvf Python-2.7.5.tgz
cd Python-2.7.5
./configure --prefix=/usr/local/python2.7
make
make install

```

### 3. Install pip and setuptools

```bash
cd /opt/netmon/pkg
unzip setuptools-41.2.0.zip
cd setuptools-41.2.0
python setup.py install

cd ..
tar -zxvf pip-19.2.3.tar.gz
cd pip-19.2.3
python setup.py install

```

### 4. Install Supervisor

```bash
cd /opt/netmon/pkg
pip install supervisor-4.0.4.tar.gz --no-index --find-links file:///opt/netmon/pkg

# Verify
/usr/local/python2.7/bin/supervisor
/usr/local/python2.7/bin/supervisorctl

# Symlink
ln -s /usr/local/python2.7/bin/supervisorctl /usr/bin/supervisorctl
ln -s /usr/local/python2.7/bin/supervisord /usr/bin/supervisord

# Start & verify
supervisord -c /etc/supervisord.conf
supervisorctl status
supervisorctl reload

```

### 5. Install pip Packages (Offline)

```bash
pip install oslo.config-6.8.1-py2.py3-none-any.whl --no-index --find-links file:///opt/netmon/pip_pkg
pip install msgpack-python-0.5.6.tar.gz --no-index --find-links file:///opt/netmon/pip_pkg/
pip install oslo.log-3.42.3-py2.py3-none-any.whl --no-index --find-links file:///opt/netmon/pip_pkg/
pip install greenlet-0.4.15.tar.gz --no-index --find-links file:///opt/netmon/pip_pkg/
pip install prettytable-0.7.2.tar.bz2 --no-index --find-links file:///opt/netmon/pip_pkg/
pip install oslo.messaging-9.5.0-py2.py3-none-any.whl --no-index --find-links file:///opt/netmon/pip_pkg/

```

## Notes

- All pip installs use `--no-index` (offline) with `--find-links` pointing to local package directory
- Python 2.7.5 is installed to `/usr/local/python2.7` to avoid overwriting the system Python
- Supervisor symlinks ensure systemd/init.d compatibility
