define(function () {
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

    return DebugLog;
});
