=========================
Lovely Webservices Status
=========================

.. image:: https://img.shields.io/pypi/v/lovely-ws-status.svg
    :target: https://pypi.org/project/lovely-ws-status/

.. image:: https://img.shields.io/pypi/pyversions/lovely-ws-status.svg
    :target: https://pypi.org/project/lovely-ws-status/

.. image:: https://travis-ci.org/lovelysystems/lovely-ws-status.svg?branch=master
    :target: https://travis-ci.org/lovelysystems/lovely-ws-status

This package provides service status utilities for Pyramid applications.
Register your own status handlers and see the service status of all registered
handlers in the ``svc_status`` Pyramid view.


Status Handler
==============

A status handler can be any method or class that checks any part of your
application stack. This can be for example a check that your database
connection is still working, or checking some external service. The status
handler must return a dict with a state property which can have the value
``OK``, ``YELLOW`` or ``RED``. Additional properties like ``detail`` can be
optionally added, but will only be displayed in the JSON SVC status view.


As Callable
-----------

Create a status handler as a python function::

    >>> from lovely.ws.status import OK
    >>> def statusHandler():
    ...     # Do whatever you need to do to check the status
    ...     return {
    ...         'state': OK
    ...     }

Register the status handler::

    >>> from lovely.ws.status import addStatusHandler
    >>> addStatusHandler('DatabaseConnection', statusHandler)

Status handlers can also be classes, just provide a ``__call__`` method::

    >>> from lovely.ws.status import RED
    >>> class StatusHandler(object):
    ...     def __call__(self):
    ...         # Do whatever you need to do to check the status
    ...         return {
    ...             'state': RED,
    ...             'detail': 'Service not available',
    ...         }
    >>> statusHandler2 = StatusHandler()
    >>> addStatusHandler('UserService', statusHandler2)


Mixin Class
-----------

To simplify the implementation of status providers there is a mixin class
which handles the state and provides logging on status changes::

    >>> from lovely.ws.status import YELLOW, GREEN
    >>> from lovely.ws.status.statehandler import StateHandlerMixin
    >>> class MyHandler(StateHandlerMixin):
    ...     def __init__(self):
    ...         self.setState(YELLOW)
    >>> myHandler = MyHandler()
    >>> addStatusHandler('myHandler', myHandler)

Now just use ``setState`` to change the state. ``setState`` allows to set any
additional property on the state::

    >>> myHandler.setState(GREEN, detail='running')


SVC Status View
===============

There's a Pyramid view that can be added to your project which creates an
endpoint to see the live service status provided by all registered status
handlers.

For the view to get registered, you need to configure this module in your application
by adding these two lines in your app factory::

    config.include('lovely.ws.status.svcstatus')
    config.scan('lovely.ws.status.svcstatus')

Calling the ``/svc_status`` endpoint will return a CSV response with an output
like this::

    DatabaseConnection OK
    UserService RED

It's also possible to receive the response in JSON format by calling the
``svc_status`` endpoint with accept header ``application/json`` or by calling
the ``svc_status.json`` endpoint. Additional properties like the detail will
only be shown in the JSON formatted output. The output will look like this::

    {
        "DatabaseConnection": {
            "state": "OK"
        },
        "UserService":{
            "state": "OK",
            "detail": "Service not available"
        }
    }

Calling the ``svc_status.prometheus`` endpoint returns the service status as
a prometheus template. The output will look like this::

    # HELP svc_status Status 0->OK, 1->YELLOW, 2->RED
    # TYPE svc_status untyped
    svc_status{name="DatabaseConnection"} 0
    # HELP svc_status Status 0->OK, 1->YELLOW, 2->RED
    # TYPE svc_status untyped
    svc_status{name="UserService"} 2

More information can be found in the `SVC status test suite
<tests/lovely/ws/status/svcstatus.rst>`_.


Probe Status View
=================

This view allows to check if the service is available and to decommission the
service. The view returns status 200 and the body ``OK`` by default.

The probe status view can be included into a Pyramid project in the
``server.py`` file by adding these two lines in your app factory::

    config.include('lovely.ws.status.probestatus')
    config.scan('lovely.ws.status.probestatus')

Decommissioning can be used to make the service unavailable for load balancers
before the service is shut down.

More information can be found in the `probe status test suite
<tests/lovely/ws/status/probestatus.rst>`_.


Development
===========

Information on how to contribute can be found in the `DEVELOPMENT.rst
<DEVELOPMENT.rst>`_ file.
