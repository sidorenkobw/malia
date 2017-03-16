define(["debuggable"], function (Debuggable) {
    class EventEmitter extends Debuggable {
        constructor() {
            super();
            this._eventCallbacks = {};
        }

        on(event, callback, isOnce) {
            this._eventCallbacks[event] = this._eventCallbacks[event] || [];
            this._eventCallbacks[event].push({
                fn: callback,
                once: !!isOnce
            });

            return this;
        }

        once(event, callback) {
            this.on(event, callback, true);
        }

        off(event, callback) {
            var events = this._eventCallbacks;

            if (!arguments.length) {
                for (var i in events) {
                    delete events[i];
                }
            } else if (callback) {
                var callbacks = events[event] || [];

                for (var i in callbacks) {
                    if (callbacks[i].fn === callback) {
                        callbacks.splice(i, 1);
                        break;
                    }
                }
            } else {
                delete this._eventCallbacks[event];
            }

            return this;
        }

        emit(event, data) {
            if (event in this._eventCallbacks) {
                var callbacks = this._eventCallbacks[event] || [];
                for (var i in callbacks) {
                    callbacks[i].fn(data, event);
                    if (callbacks[i].once) {
                        // TODO handle removing other callbacks
                        callbacks.splice(i, 1);
                        break;
                    }
                }
            }

            return this;
        }

        getEvents() {
            return _eventCallbacks;
        }
    }

    return EventEmitter;
});
