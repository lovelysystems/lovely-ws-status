===============
Status Handlers
===============

A status handler provides the status for the service status views.
It is also possible to check and/or wait for a specific state of a status
handler.


Handler Implementation
======================

A status handler is simply a callable which must provide a dict with its
current status. The content of the dict should contain a ``state`` and a
``detail`` property.

``state`` should be one of the constants::

    >>> from lovely.ws.status import RED, YELLOW, GREEN, OK

Please note that the state ``GREEN`` and ``OK`` is the same. This is for
backward compatibility and readability.

A dummy handler::

    >>> def testHandler():
    ...     return {
    ...         'state': YELLOW,
    ...         'detail': 'I am yellow'
    ...     }

Register the handler::

    >>> from lovely.ws.status import addStatusHandler
    >>> addStatusHandler('test', testHandler)

Now the status can be requested::

    >>> from lovely.ws.status import getStatus
    >>> print_dict(getStatus('test'))
    {
        "detail": "I am yellow",
        "state": "YELLOW"
    }


For classes there is the `StateHandlerMixin` class which can be used to
provide the status of the instance. This is usually be used for threads to
provide their running state as service status::

    >>> from lovely.ws.status.statehandler import StateHandlerMixin
    >>> class Checker(StateHandlerMixin):
    ...     def __init__(self):
    ...         self.setState(YELLOW)

    >>> checker = Checker()
    >>> addStatusHandler('test2', checker)
    >>> getStatus('test2')
    {'state': 'YELLOW'}

setState allows to set any additional property::

    >>> checker.setState(GREEN, detail='running')
    >>> print_dict(getStatus('test2'))
    {
        "detail": "running",
        "state": "OK"
    }

It is possible to send state changes to a logger. The logger must be assigned
to the logger property of the instance::

    >>> import logging
    >>> from io import StringIO
    >>> stream = StringIO()
    >>> handler = logging.StreamHandler(stream)
    >>> testlogger = logging.getLogger('test')
    >>> testlogger.setLevel(logging.INFO)
    >>> testlogger.addHandler(handler)
    >>> checker.logger = testlogger

    >>> checker.setState(RED, detail='stopped')
    >>> handler.flush()
    >>> stream.getvalue()
    'state change: OK -> RED "stopped"\n'


Check for Status
================

The application can check the status of a handler::

    >>> from lovely.ws.status import isInState
    >>> isInState('test', GREEN)
    False
    >>> isInState('test', YELLOW)
    True

If an unknown handler name is provided::

    >>> isInState('unknown', YELLOW)
    Traceback (most recent call last):
    KeyError: 'unknown'


Wait for Status
===============

The application can wait for a status on a handler::

    >>> from lovely.ws.status import waitForStatus

    >>> waitForStatus('test', YELLOW)
    True
    >>> waitForStatus('test', GREEN, interval=0.1, timeout=0.5)
    False

With an unknown handler::

    >>> waitForStatus('unknwon', GREEN, interval=0.1, timeout=0.5)
    False
    >>> waitForStatus('unknown', GREEN, raiseOnKeyError=True)
    Traceback (most recent call last):
    KeyError: 'unknown'


Test Clean Up
=============

Remove the registered status handler::

    >>> from lovely.ws import status
    >>> status.STATUS_HANDLERS.clear()
