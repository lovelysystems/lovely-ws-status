import time

# status enumerations
OK = 'OK'
GREEN = 'OK'
YELLOW = 'YELLOW'
RED = 'RED'


# used for prometheus templates
NUMERIC_VALUES = {
    OK: 0,
    YELLOW: 1,
    RED: 2,
}

# list of global status handlers
STATUS_HANDLERS = {}


def addStatusHandler(name, handler):
    """Register a global status handler.

    A status handler can be used for monitoring various parts of the software.
    When the SVC status view is called, the state of each registered status
    handler will be reflected.

    Properties:
      - name: The unique name of the status handler
      - handler: A function returning a dictionary with at least a 'state'
                 property. State should be one of 'OK', 'YELLOW' or 'RED'.
    """
    STATUS_HANDLERS[name] = handler


def getStatus(name):
    """Provide the current status of a handler

    raises KeyError if name is not a known status handler.
    """
    return STATUS_HANDLERS[name]()


def isInState(name, state):
    """Check if a status handler provides the given state

    raises KeyError if name is not a known status handler.
    """
    status = getStatus(name)
    return status.get('state') == state


def waitForStatus(name,
                  state,
                  interval=1,
                  timeout=None,
                  raiseOnKeyError=False):
    """Wait until service status is GREEN

    Polls the service status using isInState.

    :param name: the name of the status to poll
    :param state: the state to wait for
    :param interval: the poll interval
    :param timeout: maximum time to wait for the status
    :param raiseOnKeyError: raise KeyError if there is not handler for name
    :returns: True when handler provides state
    """
    start = time.time()
    while True:
        try:
            if isInState(name, state):
                return True
        except KeyError:
            # This happens if there is no service status handler for the name
            # registered.
            if raiseOnKeyError:
                raise
        if timeout is not None and (time.time() - start) >= timeout:
            return False
        time.sleep(interval)
