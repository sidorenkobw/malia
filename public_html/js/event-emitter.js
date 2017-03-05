class EventEmitter {
    constructor() {
        this._eventCallbacks = {};
    }
    
    on(event, callback) {
        this._eventCallbacks[event] = this._eventCallbacks[event] || [];
        this._eventCallbacks[event].push(callback);
        
        return this;
    }
    
    off(event, callback) {
        var events = this._eventCallbacks;
        
        if (!arguments.length) {
            for (var i in events) {
                delete events[i];
            }
        } else if (typeof callback != "undefined") {
            var callbacks = events[event] || [],
                i = callbacks.indexOf(callback);
            if (i > -1) {
                callbacks.splice(i, 1);
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
                console.log(callbacks[i])
                callbacks[i](data, event);
            }
        }
        
        return this;
    }
    
    getEvents() {
        return _eventCallbacks;
    }
}
