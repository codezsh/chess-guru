class EventBus:
    def __init__(self):
        self._events = {}

    def on(self, event_name, callback):
        """ Register an event listener. """
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(callback)

    def emit(self, event_name):
        """ Trigger an event without arguments. """
        if event_name in self._events:
            for callback in self._events[event_name]:
                callback()

    def emit_with_arg(self, event_name, *args, **kwargs):
        """ Trigger an event with arguments. """
        if event_name in self._events:
            for callback in self._events[event_name]:
                callback(*args, **kwargs)

# main event bus
AppBus = EventBus()