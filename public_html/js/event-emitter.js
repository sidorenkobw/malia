class DebugLog {
    constructor() {
        this.debugLevel = null;
        this.debugTag = null;
    }
    
    setDebugLevel(level) {
        // 'log', 'error', 'warn', 'debug', 'info', 'verbose'
        this.debugLevel = level.toLowerCase();
    }
    
    setDebugTag(tag) {
        this.debugTag = tag;
    }
    
    data(msg, level, tag) {
        var isAllowed = true,
            level = level || "log";
        
        if (this.debugLevel && this.debugLevel != level) {
            isAllowed = false;
        }
        
        if (this.debugTag && this.debugTag != tag) {
            isAllowed = false;
        }
        
        if (isAllowed) {
            console.log(level.toUpperCase() + ":" + "[" + tag+ "]:", msg);
        }
    }
}

class Debuggable {
    constructor() {
        this.debugLog = null;
    }
    
    setDebugLog(debugLog) {
        this.debugLog = debugLog;
    }
    
    debug(data, level, tag) {
        if (this.debugLog) {
            this.debugLog.data(data, level, tag);
        }
    }
}

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
