===============
SVC Status View
===============

The SVC status provides information about the current status of the service.
The status can be requested as a CSV text file, as json data or as prometheus
template.

Including in Pyramid Project
============================

This view can simply be integrated into your Pyramid project by adding the
include and the scan in the app factory of your server.py file::

    config.include('lovely.ws.status.svcstatus')
    config.scan('lovely.ws.status.svcstatus')

The endpoint will then be available at these endpoints::

    /svc_status
    /svc_status.csv
    /svc_status.json
    /svc_status.prometheus


SVC Status
==========

A plain request on the svc status view provides the CSV version of the status::

    >>> from lovely.ws.status.svcstatus import svc_status_view
    >>> from pyramid.testing import DummyRequest
    >>> request = DummyRequest()
    >>> response = svc_status_view(request)
    >>> response.headers.get('Content-Type')
    'text/csv; charset=UTF-8'
    >>> response.status
    '200 OK'

There is no data because there is no handler installed::

    >>> response.body
    b''

Add a status handler. As parameters provide a name of the handler and a
function returning the current state::

    >>> from lovely.ws.status import RED, YELLOW, OK
    >>> def status_handler():
    ...     return {'state': OK}

    >>> from lovely.ws.status import addStatusHandler
    >>> addStatusHandler('status1', status_handler)

Now the status of the handler is provided by the svc status view::

    >>> response = svc_status_view(request)
    >>> print(response.body.decode('utf-8'))
    status1	OK

Multiple handlers can be added::

    >>> addStatusHandler('status2', status_handler)
    >>> addStatusHandler('status3', status_handler)
    >>> response = svc_status_view(request)
    >>> print(response.body.decode('utf-8'))
    status1	OK
    status2	OK
    status3	OK

The view can alternatively be called with the '.csv' extension::

    >>> request = DummyRequest()
    >>> request.matchdict = {'type': '.csv'}
    >>> response = svc_status_view(request)
    >>> print(response.body.decode('utf-8'))
    status1	OK
    status2	OK
    status3	OK


Status As JSON
==============

If the view is called with the accept header set to 'application/json', a JSON
result is responded::

    >>> request = DummyRequest()
    >>> request.headers = {'accept': 'application/json'}
    >>> response = svc_status_view(request)
    >>> print(response.body.decode('utf-8'))
    {"status1":{"state":"OK"},"status2":{"state":"OK"},"status3":{"state":"OK"}}
    >>> response.headers.get('Content-Type')
    'application/json'

The view can alternatively be called with the '.json' extension::

    >>> request = DummyRequest()
    >>> request.matchdict = {'type': '.json'}
    >>> response = svc_status_view(request)
    >>> response.headers.get('Content-Type')
    'application/json'
    >>> print(response.body.decode('utf-8'))
    {"status1":{"state":"OK"},"status2":{"state":"OK"},"status3":{"state":"OK"}}

Additional status info can only be provided in the JSON view::

    >>> def informative_status_handler():
    ...     return {'state': OK, 'detail': 'some more information'}
    >>> addStatusHandler('status2', informative_status_handler)
    >>> response = svc_status_view(request)
    >>> print(response.body.decode('utf-8'))
    {"status1":{"state":"OK"},"status2":{"state":"OK","detail":"some more information"},"status3":{"state":"OK"}}


Prometheus Status
=================

By using the `.prometheus` extension it's possible to retrieve the SVC status
in the prometheus exposition format (text).

Mock states for status 2 and 3::

    >>> def status_handler_yellow():
    ...     return {'state': YELLOW, 'labels': 'not a dict'}
    >>> def status_handler_red():
    ...     return {'state': RED, 'labels': {"errors": 7, "good": 42}}
    >>> addStatusHandler('status2', status_handler_yellow)
    >>> addStatusHandler('status3', status_handler_red)

The status can be requested in prometheus exposition format::

    >>> request = DummyRequest()
    >>> request.matchdict = {'type': '.prometheus'}
    >>> response = svc_status_view(request)
    >>> response.headers.get('Content-Type')
    'text/plain; version=0.0.4; charset=UTF-8'
    >>> print(response.body.decode('utf-8'))
    # HELP svc_status Status 0->OK, 1->YELLOW, 2->RED
    # TYPE svc_status untyped
    svc_status{name="status1"} 0
    # HELP svc_status Status 0->OK, 1->YELLOW, 2->RED
    # TYPE svc_status untyped
    svc_status{name="status2"} 1
    # HELP svc_status Status 0->OK, 1->YELLOW, 2->RED
    # TYPE svc_status untyped
    svc_status{name="status3"} 2
    svc_status{name="status3_errors"} 7
    svc_status{name="status3_good"} 42
    ...

Because the test environment has prometheus_client installed additional
prometheus metrics are provided::

    >>> print(response.body.decode('utf-8'))
    # HELP ...
    ...
    # HELP python_info Python platform information
    # TYPE python_info gauge
    python_info{implementation="CPython",...

The last metric must end with a new line::

    >>> response.body.endswith(b'\n')
    True

Prometheus metrics are also added if available::

    >>> from prometheus_client import Counter
    >>> c = Counter('test', 'A test counter')
    >>> c.inc()
    >>> response = svc_status_view(request)
    >>> print(response.body.decode('utf-8'))
    # HELP ...
    ...
    # HELP test A test counter
    # TYPE test counter
    test 1.0
    <BLANKLINE>

    >>> c.inc()
    >>> response = svc_status_view(request)
    >>> print(response.body.decode('utf-8'))
    # HELP ...
    ...
    # HELP test A test counter
    # TYPE test counter
    test 2.0
    <BLANKLINE>


Test Clean Up
=============

Remove the registered status handler::

    >>> from lovely.ws import status
    >>> status.STATUS_HANDLERS.clear()
