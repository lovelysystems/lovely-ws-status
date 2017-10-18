# status enumerations
OK = 'OK'
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
