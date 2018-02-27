# -*-coding: utf-8 -*-

"""
Author          : Arijit Basu <sayanarijit@gmail.com>
Website         : https://sayanarijit.github.io
"""

import json
import requests
import argparse

router_endpoints = {
    'application_router',
    'detailnav_router',
    'devicedumpload_router',
    'devicemanagement_router',
    'device_router',
    'evclasses_router',
    'evconsole_router',
    'host_router',
    'introspection_router',
    'jobs_router',
    'manufacturers_router',
    'messaging_router',
    'mib_router',
    'monitor_router',
    'network_6_router',
    'network_router',
    'process_router',
    'properties_router',
    'report_router',
    'search_router',
    'service_router',
    'settings_router',
    'template_router',
    'triggers_router',
    'users_router',
    'zenpack_router'
}


class InvalidRouterEndpointError(Exception):
    def __init__(self, router):
        Exception.__init__(self,
            '"{}" is not listed as a valid router endpoint.\nTry one of: {}'.format(router, ', '.join(router_endpoints)))


class InvalidActionError(Exception):
    def __init__(self, action):
        Exception.__init__(self, '"{}" is not a valid action'.format(action))


class ZenossClient(object):
    """
    Zenoss API client for python
    """
    def __init__(self, host, user, passwd, dmd='/zport/dmd', verify=False):
        self.baseurl = 'https://' + host + dmd
        self.session = requests.Session()
        self.session.auth = (user, passwd)
        self.session.headers.update({'content-type': 'application/json'})
        self.session.verify = verify

    def __getattr__(self, attr):
        """
        Dynamically create endpoint object
        """
        if attr not in router_endpoints:
            raise InvalidRouterEndpointError(attr)
        return ZenossEndpoint(
            endpoint=self.baseurl + '/' + attr,
            session=self.session
        )


class ZenossEndpoint(object):
    """
    Zenoss endpoint
    """
    def __init__(self, endpoint, session):
        self.endpoint = endpoint
        self.session = session

    def __getattr__(self, attr):
        """
        Dynamically create method object
        """
        if 'Router' not in attr or attr.replace('Router', '').lower() not in self.endpoint:
            raise InvalidActionError(attr)
        return ZenossAction(
            action = self.endpoint + '/' + attr,
            session = self.session
        )


class ZenossAction(object):
    """
    Zenoss action
    """
    def __init__(self, action, session):
        self.action = action
        self.session = session

    def __getattr__(self, attr):
        """
        Dynamically create method object
        """
        self.method = self.action + '/' + attr
        return self.zenoss_method

    def zenoss_method(self, timeout=None, **kwargs):
        """
        Do the actual query
        """
        result = self.session.post(
            self.method,
            data = json.dumps(kwargs),
            timeout = timeout
        )
        return result.json()


def zenoss_client():
    """
    Command-line interface for zenoss client
    """
    parser = argparse.ArgumentParser(prog=__file__, description=None)
    parser.add_argument('router_endpoint', options=router_endpoints)
    parser.add_argument('action')
    parser.add_argument('method')
    parser.add_argument('data', nargs='?', type=json.loads, default={})
    parser.add_argument('-h','--host')
    parser.add_argument('-u','--user')
    parser.add_argument('-p','--passwd')
    parser.add_argument('-t','--timeout', default=None)

    parsed = parser.parse_args()

    zenoss = ZenossClient(host=parsed.host, user=parsed.user, passwd=parsed.passwd)
    router_endpoint = getattr(zenoss, parsed.router_endpoint)
    action = getattr(router_endpoint, parsed.action)
    method = getattr(action, parser.method)
    method(timeout=parsed.timeout, **parsed.data)
