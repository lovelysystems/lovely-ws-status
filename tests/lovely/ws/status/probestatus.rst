=================
Probe Status View
=================

The probestatus view contains a simple view for probing the status.

Including in Pyramid Project
============================

This view can simply be integrated into your Pyramid project by adding the
include and the scan in the app factory of your server.py file::

    config.include('lovely.ws.status.probestatus')
    config.scan('lovely.ws.status.probestatus')

The endpoint will then be available at this endpoint::

    /probe_status


The Probe Status View
=====================

The probestatus view returns 'OK' if it is called::

    >>> from lovely.ws.status.probestatus import probe_status_view
    >>> from pyramid.testing import DummyRequest
    >>> request = DummyRequest()
    >>> response = probe_status_view(request)
    >>> response.body
    b'OK'
    >>> response.headers.get('Content-Type')
    'text/plain; charset=UTF-8'
    >>> response.status
    '200 OK'


Controlling The Probe Status
============================

To be able to shut down an application server it is possible to control the
probe_status response. This can be done by posting on the probe_status
endpoint and providing the get parameter "body". "body" can be any string. If
the string is not "OK" the probe_status endpoint will return http status 503
and the "body" parameter as the body::

    >>> request = DummyRequest()
    >>> request.method = 'POST'
    >>> request.GET = {'body': 'OFF'}
    >>> res = probe_status_view(request)
    >>> print(res.status)
    200 OK
    >>> print(res.body)
    b'OFF'

    >>> request = DummyRequest()
    >>> res = probe_status_view(request)
    >>> print(res.status)
    503 Service Unavailable
    >>> print(res.body)
    b'OFF'

Setting the body to "OK" changes the response status code to 200::

    >>> request = DummyRequest()
    >>> request.method = 'POST'
    >>> request.GET = {'body': 'OK'}
    >>> res = probe_status_view(request)
    >>> print(res.status)
    200 OK
    >>> print(res.body)
    b'OK'

    >>> request = DummyRequest()
    >>> res = probe_status_view(request)
    >>> print(res.status)
    200 OK
    >>> print(res.body)
    b'OK'
