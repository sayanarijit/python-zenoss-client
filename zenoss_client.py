# -*-coding: utf-8 -*-

"""
Author          : Arijit Basu <sayanarijit@gmail.com>
Website         : https://sayanarijit.github.io
"""

from __future__ import absolute_import, unicode_literals
import json
import requests
import argparse

VERSION = 'v0.0.1'

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
            kwargs.update({'action': self.action, 'method': method, 'tid': 1})
            return self.session.post(
                self.endpoint,
                data = json.dumps(kwargs),
                timeout = timeout
            ).json()
        return wrapped

    def __getattr__(self, attr):
        """
        Dynamically create method object
        """
        return self.method(attr)


def cli():
    """
    Command-line interface for zenoss client
    """
    parser = argparse.ArgumentParser(prog=__file__, description='Command-line interface for zenoss client')
    parser.add_argument('endpoint', options=router_endpoints)
    parser.add_argument('action')
    parser.add_argument('method')
    parser.add_argument('data', nargs='?', type=json.loads, default={})
    parser.add_argument('-h','--host')
    parser.add_argument('-u','--user')
    parser.add_argument('-p','--passwd')
    parser.add_argument('-t','--timeout', default=None)
    parser.add_argument('-i','--indent', type=int, default=4)
    parser.add_argument('--version', action='version', version='%(prog)s '+VERSION)

    p = parser.parse_args()

    zenoss = ZenossClient(host=p.host, user=p.user, passwd=p.passwd)
    result = zenoss.endpoint(p.endpoint).action(p.action).method(p.method)(timeout=p.timeout, **p.data)
    print(json.dumps(result, indent=p.indent))


if __name__ == '__main__':

    # Enter CLI
    cli()
