requirejs.config({
    baseUrl : "/js",
    shim : {
        bootstrap : ["jquery"],
        bootstrapnotify : ["jquery", "bootstrap"]
    },
    paths : {
        jquery     : "/lib/jquery/jquery-3.1.1.min",
        bootstrap  : "/lib/bootstrap/3.3.7/js/bootstrap.min",
        text       : "/lib/require/plugins/text",
        bootstrapnotify : "/lib/bootstrap-notify/js/bootstrap-notify"
    },
    urlArgs : "build=" + malia.cfg.build
});

define("malia", malia);

define([
    "malia",
    "debug-log",
    "view/auth",
    "jquery"
], function (
    malia,
    DebugLog,
    AuthView,
    $
) {
    $.abc = 123;
    malia.debugLog = new DebugLog(malia);
    malia.auth = new AuthView(malia);
    malia.callback && malia.callback();
});
