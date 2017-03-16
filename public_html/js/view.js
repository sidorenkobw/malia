define(["event-emitter", "jquery"], function (EventEmitter, $) {
    class View extends EventEmitter {
        constructor() {
            super();

            this.$overlayContainer = $(".overlayContainer");
            this.$overlayText = $(".overlayText");
        }

        showNotification(type, msg) {
            $('.top-right').notify({
                type: type,
                message: { text: msg }
            }).show();
        }

        showOverlay(msg) {
            this.$overlayText.text(msg);
            this.$overlayContainer.show();
        }

        hideOverlay() {
            setTimeout((function () {
                this.$overlayContainer.hide();
            }).bind(this), 300);
        }

        run() {}
    }

    return View;
});
