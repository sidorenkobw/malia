class LearnView {
    constructor() {
        /* idle|record|edit */
        this.mode = "idle";
        this.activeWordIndex = 0;
        this.$words = null;
        this.isFullscreen = false;
        this.recordTimeout = 6000;
        this.recordTimer = null;
        
        this.initEls();
        this.initButtons();
        this.initKeyboardEvents();
        this.initEditor();
        this.initTextContainer();
        
        this.render();
    }
    
    initEls() {
        this.$app = $("#learnApp");
        this.$overlayContainer = $(".overlayContainer");
        this.$overlayText = $(".overlayText");
        this.$textContainer = $("#learnTextContainer");
        this.$textEditor = $("#learnTextEditor");
        this.$btnRetry   = $("#btnLearnRetry");
        this.$btnToggleRecording = $("#btnLearnToggleRecording");
        this.$btnNext = $("#btnLearnNext");
        this.$btnToggleEdit = $("#btnLearnToggleEdit");
        this.$btnToggleFullscreen = $("#btnFullScreen");
    }
    
    initTextContainer() {
        this.$textContainer.on("click", this.onClickTextContainer.bind(this));
    }
    
    initEditor() {
        this.$textEditor
            .removeClass("hidden")
            .val(this.loadTextFromStorage())
            .hide();
            
        this.updateText();
        this.onChangeMode();
    }
    
    initKeyboardEvents() {
        $(document).on("keydown", this.onKeyPressed.bind(this));
    }
    
    initButtons() {
        this.$btnToggleEdit.click(this.onClickToggleEdit.bind(this));
        this.$btnToggleRecording.click(this.onClickToggleRecording.bind(this));
        this.$btnNext.click(this.onClickNext.bind(this));
        this.$btnRetry.click(this.onClickRetry.bind(this));
        this.$btnToggleFullscreen.click(this.onClickToggleFullscreen.bind(this));
        
        $(document).click((function(e) {
            if (this.mode == "edit" && e.target !== this.$textEditor.get(0)) {
                e.preventDefault();
                this.setMode("idle");
            }
        }).bind(this));
    }
    
    onKeyPressed(e) {
        if (e.which == 27) {
            if (this.mode != "idle") {
                this.setMode("idle");
            }
            
            if (this.isFullscreen) {
                this.setFullscreen(false);
            }
        }
    }
    
    onChangeMode(old) {
        if (old == "edit") {
            this.showOverlay("Analyzing text...")
            setTimeout((function () {
                this.updateText();
                this.hideOverlay();
            }).bind(this), 10);
        }
        
        if (old == "record") {
            this.stopRecording();
            this.deleteCurrentRecord();
        }
            
        if (this.mode == "idle") {
            this.$textContainer.show();
            this.$textEditor.hide();
            
            this.$btnToggleRecording.prop("disabled", false);
            this.$btnRetry.prop("disabled", true);
            this.$btnNext.prop("disabled", true);
        } if (this.mode == "edit") {
            this.$textContainer.hide();
            this.$textEditor.show();
            
            this.$btnToggleRecording.prop("disabled", true);
            this.$btnRetry.prop("disabled", true);
            this.$btnNext.prop("disabled", true);
            this.$textEditor.focus();
        } else if (this.mode == "record"){
            this.startRecording();
        }
        
        this.updateButtons();
    }
    
    onClickTextContainer(e) {
        var $target = $(e.target);
        if ($target.is("span")) {
            if (this.mode == "record") {
                this.stopRecording();
                this.deleteCurrentRecord();
            }
            
            this.setActiveWord(this.$words.index($target));
            
            if (this.mode == "record") {
                this.startRecording();
            }
        }
    }
    
    onClickToggleFullscreen(e)
    {
        this.setFullscreen(!this.isFullscreen);
    }
    
    onClickToggleEdit(e) {
        e.stopPropagation();
        this.setMode(this.mode == "edit" ? "idle" : "edit");
    }
    
    onClickToggleRecording(e) {
        this.setMode(this.mode == "record" ? "idle" : "record");
    }
    
    onClickNext(e) {
        this.stopRecording();
        this.uploadActiveWord(this.getActiveWordEl().text());
        
        if (this.$words.length == this.activeWordIndex+1) {
            this.setMode("idle");
            this.setActiveWord(0);
        } else {
            this.setActiveWord(this.activeWordIndex+1)
            this.startRecording();
        }
    }
    
    onClickRetry(e) {
        this.stopRecording();
        this.deleteCurrentRecord();
        this.startRecording();
    }

    getActiveWordEl()
    {
        return this.$words.eq(this.activeWordIndex);
    }
    
    setMode(mode) {
        var old = this.mode;
        this.mode = mode;
        this.onChangeMode(old);
    }
    
    setActiveWord(index)
    {
        this.activeWordIndex = index;
        this.updateActiveWord();
    }
    
    setFullscreen(flag)
    {
        this.isFullscreen = !!flag;
        
        if (this.isFullscreen) {
            this.$app.addClass("fullscreen");
        } else {
            this.$app.removeClass("fullscreen");
        }
        
        this.updateButtons();
    }
    
    saveTextToStorage(text) {
        localStorage.setItem("text", text);
    }
    
    loadTextFromStorage() {
        return localStorage.getItem("text");
    }
    
    updateText() {
        var text = this.$textEditor.val();
        this.saveTextToStorage(text);
        this.updateTextContainer(text);
    }
    
    updateButtons()
    {
        if (this.mode == "edit") {
            this.$btnToggleEdit.find(".caption").eq(0).text("Finish Editing");
            this.$btnToggleRecording.prop("disabled", true);
            this.$btnToggleEdit.toggleClass("btn-warning", true);
        } else {
            this.$btnToggleEdit.find(".caption").eq(0).text("Edit Text");
            this.$btnToggleEdit.toggleClass("btn-warning", false);
            this.$btnToggleRecording.prop("disabled", !this.$words.length);
        }
        
        if (this.mode == "record") {
            this.$btnToggleRecording.find(".caption").eq(0).text("Stop Recording");
            this.$btnToggleRecording.removeClass("btn-primary");
            this.$btnToggleRecording.addClass("btn-danger");
            this.$btnRetry.prop("disabled", false);
            this.$btnNext.prop("disabled", false);
        } else {
            this.$btnToggleRecording.find(".caption").eq(0).text("Start Recording");
            this.$btnToggleRecording.addClass("btn-primary");
            this.$btnToggleRecording.removeClass("btn-danger");
            this.$btnRetry.prop("disabled", true);
            this.$btnNext.prop("disabled", true);
        }
        
        if (this.isFullscreen) {
            this.$btnToggleFullscreen.addClass("btn-warning");
            this.$btnToggleFullscreen.removeClass("btn-default");
        } else {
            this.$btnToggleFullscreen.removeClass("btn-warning");
            this.$btnToggleFullscreen.addClass("btn-default");
        }
    }
    
    uploadActiveWord(word) {
        console.log("Upload word: " + word)
    }
    
    startRecording() {
        console.log("Start recording");
        
        this.scrollToActiveWord();
        this.recordTimer = setTimeout((function () {
            this.setMode("idle");
            this.showNotification("Recording timeout");
        }).bind(this), this.recordTimeout);
    }
    
    stopRecording() {
        clearTimeout(this.recordTimer);
        console.log("Stop recording");
    }
    
    deleteCurrentRecord()
    {
        console.log("Delete current record");
    }
    
    textToHtml(text) {
        var mask = [
            "[a-zA-Z]+'[a-z]+", // shortened words: Don't
            "[a-zA-Z0-9]+",     // words, numbers and words with numbers: hi 2 html5 i18n
            "[+=*%@$&#]"        // symbols
        ].join("|");
        
        var mask = new RegExp("(" + mask + ")");
        text = text
            .split(mask)
            .map(function (word) {
                var escapedWord = $("<span>").text(word).html();
                if (word.match(mask)) {
                    escapedWord = "<span>" + escapedWord + "</span>"
                }
                
                return escapedWord;
            })
            .join("")
            .split(/\n/)
            .join("<br>");

        return text;
    }
    
    updateTextContainer(text) {
        text = this.textToHtml(text);
        
        this.$textContainer
            .empty()
            .html(text);
            
        this.$words = this.$textContainer.find("span");
        this.setActiveWord(0);
    }
    
    scrollToActiveWord()
    {
        var $el = this.getActiveWordEl();
        
        if (!$el.length) {
            return;
        }
        
        var offsetTop = $el.offset().top - this.$textContainer.offset().top,
            scrollTop = this.$textContainer.scrollTop(),
            height = this.$textContainer.height();
            
        if ((offsetTop > height - 30) || (offsetTop < 5)) {
            this.$textContainer.animate({scrollTop: scrollTop + offsetTop - 3}, 500);
        }
    }
    
    showNotification(msg) {
        $('.top-right').notify({
            type: "danger",
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
    
    updateActiveWord() {
        this.$words.removeClass("active");
        this.getActiveWordEl().addClass("active");
        this.scrollToActiveWord();
    }
    
    render() {
        this.hideOverlay();
    }
}

$(function () {
    var view = new LearnView();
});
