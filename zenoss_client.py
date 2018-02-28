# -*-coding: utf-8 -*-

"""
Author          : Arijit Basu <sayanarijit@gmail.com>
Website         : https://sayanarijit.github.io
"""

from __future__ import absolute_import, unicode_literals
import json
import requests


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
        self.session.tid = 0

    def endpoint(self, endpoint):
        """
        Return endpoint object
        """
        if endpoint not in router_endpoints:
            raise InvalidRouterEndpointError(endpoint)
        return ZenossEndpoint(
            endpoint=self.baseurl + '/' + endpoint,
            session=self.session
        )

    def __getattr__(self, attr):
        """
        Dynamically create endpoint
        """
        return self.endpoint(attr)


class ZenossEndpoint(object):
    """
    Zenoss endpoint
    """
    def __init__(self, endpoint, session):
        self.endpoint = endpoint
        self.session = session

    def action(self, action):
        """
        Return action object
        """
        if 'Router' not in action or action.replace('Router', '').lower() not in self.endpoint:
            raise InvalidActionError(action)
        return ZenossAction(
            endpoint = self.endpoint,
            action = action,
            session = self.session
        )

    def __getattr__(self, attr):
        """
        Dynamically create action object
        """
        return self.action(attr)


class ZenossAction(object):
    """
    Zenoss action
    """
    def __init__(self, endpoint, action, session):
        self.endpoint = endpoint
        self.action = action
        self.session = session

    def method(self, method):
        """
        Return callable method
        """
        def wrapped(timeout=None, **kwargs):
            payload = {'action': self.action, 'method': method,
                    'tid': self.session.tid, 'data': [kwargs]}
            result = self.session.post(
                self.endpoint,
                data = json.dumps(payload),
                timeout = timeout
            )
            self.session.tid += 1
            return result.json()
        return wrapped

    def __getattr__(self, attr):
        """
        Dynamically create method object
        """
        return self.method(attr)

