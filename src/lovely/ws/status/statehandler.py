

class StateHandlerMixin(object):
    """A mixin for threads to provide svc status data

    Derive from StateHandlerMixin and register as a handler.
    Use setState to update the current state.
    Set `logger` to a logger and state changes will be logged as INFO.
    """

    logger = None
    __state = None

    def setState(self, state, **kwargs):
        """Set the internal state and log changes
        """
        old_state = self.__state and self.__state.get('state')
        self.__state = {
            "state": state,
        }
        self.__state.update(kwargs)
        if self.logger is not None and old_state != state:
            self.logger.info('state change: %s -> %s "%s"' % (
                old_state, state, kwargs.get('detail')))

    def __call__(self):
        """Provides the current connection status for svc_status
        """
        return self.__state or {}
