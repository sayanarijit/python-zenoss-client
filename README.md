# python-zenoss-client

[![PyPI version](https://img.shields.io/pypi/v/python-zenoss-client.svg)](https://pypi.python.org/pypi/python-zenoss-client)
[![Build Status](https://travis-ci.org/sayanarijit/python-zenoss-client.svg?branch=master)](https://travis-ci.org/sayanarijit/python-zenoss-client)

Zenoss API client for python


### Installation

```bash
pip install python-zenoss-client
```

### Usage

* Connect

```python
from zenoss_client import ZenossClient

api = ZenossClient(host="localhost", user="zenuser", passwd="*****")
```

* API call: The long way

```python
endpoint = api.endpoint('device_router')
action = endpoint.action('DeviceRouter')
method = action.method('getDevices')

method(params={'name': 'testdevice'})
```

* API call: The sorter way

```python
api.endpoint('device_router').action('DeviceRouter').method('getDevices')(params={'name': 'testdevice'})
```

* API call: The sortest way

```python
api.device_router.DeviceRouter.getDevices(params={'name': 'testdevice'})
```

* With timeout

```python
api.device_router.DeviceRouter.getDevices(params={'name': 'testdevice'}, timeout=10)
```

### Documentation

This module is inspired by [json_api.sh](http://wiki.zenoss.org/Working_with_the_JSON_API#v5_version_of_the_json_api.sh) SHELL script published on [zenoss official wiki](http://wiki.zenoss.org)

For full documentation of zenoss API, kindly refer to the link below:
### [zenoss official documentation](https://www.zenoss.com/services-support/documentation/zenoss-json-api-0)

* Conventional naming of routers
```
Products.Zuul.routers.device -> device_router
Products.Zuul.routers.users -> users_router
Products.Zuul.routers.triggers -> triggers_router
```
