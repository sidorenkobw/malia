define(function () {
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

    return Debuggable;
});
