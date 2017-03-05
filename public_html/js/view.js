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
    
    debug(msg, level) {
        console.log(msg)
    }
}
