class LearnView extends View {
    constructor() {
        super();
        
        /* idle|record|edit */
        this.mode = "idle";
        this.activeWordIndex = 0;
        this.$words = null;
        this.isFullscreen = false;
        this.recordTimeout = 6000;
        this.recordTimer = null;
        
        this.initEls();
        this.initEvents();
        this.initButtons();
        this.initKeyboardEvents();
        this.initEditor();
        this.initTextContainer();
        
        this.render();
    }
    
    initEvents() {
        var events = {
            "mode": this.onChangeMode,
            
            "mode-idle-on":  this.onModeIdleOn,
            "mode-idle-off": this.onModeIdleOff,
            
            "mode-record-on":  this.onModeRecordOn,
            "mode-record-off": this.onModeRecordOff,
            
            "mode-edit-on":  this.onModeEditOn,
            "mode-edit-off": this.onModeEditOff,
            
            "fullscreen-on":  this.onFullscreenOn,
            "fullscreen-off": this.onFullscreenOff,
            
            "word-next":   this.onWordNext,
            "word-retry":  this.onWordRetry,
            "word-skip":   this.onWordSkip,
            "active-word": this.onActiveWord,
            
            "record-start":  this.onRecordStart,
            "record-stop":   this.onRecordStop,
            "record-delete": this.onRecordDelete,
        };
        
        for (var event in events) {
            this.on(event, events[event].bind(this));
        }
    }
    
    initEls() {
        this.$app = $("#learnApp");
        this.$textContainer = $("#learnTextContainer");
        this.$textEditor = $("#learnTextEditor");
        this.$btnRetry   = $("#btnLearnRetry");
        this.$btnToggleRecording = $("#btnLearnToggleRecording");
        this.$btnNext = $("#btnLearnNext");
        this.$btnSkip = $("#btnSkipWord");
        this.$btnToggleEdit = $("#btnLearnToggleEdit");
        this.$btnToggleFullscreen = $("#btnFullScreen");
    }
    
    initTextContainer() {
        this.$textContainer.on("click", this.onClickTextContainer.bind(this));
    }
    
    initEditor() {
        var text = this.loadTextFromStorage();
        
        if (null !== text && typeof text != "undefined") {
            this.$textEditor.val(text);
        }
        
        this.$textEditor
            .removeClass("hidden")
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
        this.$btnSkip.click(this.onClickSkip.bind(this));
        this.$btnToggleFullscreen.click(this.onClickToggleFullscreen.bind(this));
    }
    
    skipActiveWord() {
        this.emit("word-skip");
        
        this.stopRecording();
        this.deleteCurrentRecord();
        
        this.setActiveWord(this.activeWordIndex+1);
    }
    
    switchActiveWord(i) {
        this.stopRecording();
        this.deleteCurrentRecord();
        
        this.setActiveWord(i);
    }
    
    setActiveWord(i) {
        if (this.$words.length == i) {
            this.setMode("idle");
            this.activeWordIndex = 0;
            this.emit("active-word");
            this.showNotification("success", "End of text.");
        } else {
            this.activeWordIndex = i;
            this.emit("active-word");
            if (this.mode == "record") {
                this.startRecording();
            }
        }
    }
    
    onKeyPressed(e) {
        var $target = $(e.target);
        
        if (e.which == 27) {
            // esc
            if (this.mode != "idle") {
                this.setMode("idle");
            }
        } else if (e.which == 13 && e.ctrlKey) {
            // ctrl + enter
            if (this.mode != "record") {
                e.preventDefault();
                this.setMode("record");
            }
        } else if (e.which == 13 && e.altKey) {
            // alt + enter
            e.preventDefault();
            this.setFullscreen(!this.isFullscreen);
        } else if (e.which == 32 || e.which == 13) {
            // space or enter
            if (this.mode == "record") {
                e.preventDefault();
                this.$btnNext.click();
            }
        } else if (e.which == 8) {
            // backspace
            if (this.mode == "record") {
                e.preventDefault();
                this.$btnRetry.click();
            }
        }
    }
    
    onClickTextContainer(e) {
        var $target = $(e.target);
        if ($target.is("span")) {
            this.switchActiveWord(this.$words.index($target));
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
        this.emit("word-next");
    }
    
    onClickRetry(e) {
        this.emit("word-retry");
    }

    onClickSkip(e) {
        this.skipActiveWord();
    }

    setMode(mode) {
        var old = this.mode;
        this.mode = mode;
        this.emit("mode", old);
    }
    
    onChangeMode(old) {
        this.emit("mode-" + old + "-off");
        this.emit("mode-" + this.mode + "-on");
    }
    
    onModeIdleOn() {
        this.debug("Mode idle on");
    }
    
    onModeIdleOff() {
        this.debug("Mode idle off");
    }
    
    onModeRecordOn() {
        this.debug("Mode record on");
        
        this.$btnToggleRecording
            .removeClass("btn-primary")
            .addClass("btn-danger")
            .find(".caption")
                .eq(0)
                .text("Stop Recording");
            
        this.$btnRetry.prop("disabled", false);
        this.$btnNext.prop("disabled", false);
        this.$btnSkip.prop("disabled", false);
        
        this.$btnNext.focus();
        
        this.startRecording();
    }
    
    onModeRecordOff() {
        this.debug("Mode record off");
        
        this.$btnToggleRecording
            .addClass("btn-primary")
            .removeClass("btn-danger")
            .find(".caption")
                .eq(0)
                .text("Start Recording");

        this.$btnRetry.prop("disabled", true);
        this.$btnNext.prop("disabled", true);
        this.$btnSkip.prop("disabled", true);
        
        this.stopRecording();
        this.deleteCurrentRecord();
    }
    
    onModeEditOn() {
        this.debug("Mode edit on");
        
        this.$textEditor.show();
        this.$textContainer.hide();
        this.$textEditor.focus();
        
        this.$btnToggleEdit
            .toggleClass("btn-warning", true)
            .find(".caption")
                .eq(0)
                .text("Finish Editing");
    }
    
    onModeEditOff() {
        this.debug("Mode edit off");
        
        this.$textEditor.hide();
        this.$textContainer.show();
        
        this.$btnToggleEdit
            .toggleClass("btn-warning", false)
            .find(".caption")
                .eq(0)
                .text("Edit Text");
        
        this.showOverlay("Analyzing text...")
        setTimeout((function () {
            this.updateText();
            this.saveTextToStorage(this.$textEditor.val());
            this.hideOverlay();
        }).bind(this), 10);
    }

    setFullscreen(flag) {
        this.isFullscreen = !!flag;
        this.emit("fullscreen-" + (this.isFullscreen ? "on" : "off"));
    }
    
    onFullscreenOn() {
        this.debug("Fullscreen on");
        
        this.$app.addClass("fullscreen");
        this.$btnToggleFullscreen.addClass("btnChecked");
    }
    
    onFullscreenOff() {
        this.debug("Fullscreen off");
        
        this.$app.removeClass("fullscreen");
        this.$btnToggleFullscreen.removeClass("btnChecked");
    }
    
    onActiveWord() {
        this.debug("Active word changed");
        this.$words.removeClass("active");
        this.getActiveWordEl().addClass("active");
        this.scrollToActiveWord();
    }
    
    onWordNext() {
        this.stopRecording();
        this.uploadActiveWord(this.getActiveWordEl().text());
        this.setActiveWord(this.activeWordIndex+1);
    }
    
    onWordRetry() {
        this.debug("Retry word");
        
        this.stopRecording();
        this.deleteCurrentRecord();
        this.startRecording();
    }
    
    onWordSkip() {
        this.debug("Skip word");
    }
    
    onRecordStart() {
        this.debug("Start recording");
        
        this.scrollToActiveWord();
        this.recordTimer = setTimeout((function () {
            this.setMode("idle");
            this.showNotification("danger", "Recording timeout");
        }).bind(this), this.recordTimeout);
        
    }
    onRecordStop() {
        this.debug("Stop recording");
        clearTimeout(this.recordTimer);
    }
    
    onRecordDelete() {
        this.debug("Delete current record");
    }
    
    getActiveWordEl() {
        return this.$words.eq(this.activeWordIndex);
    }
    
    saveTextToStorage(text) {
        localStorage.setItem("text", text);
    }
    
    loadTextFromStorage() {
        return localStorage.getItem("text");
    }
    
    updateText() {
        var text = this.$textEditor.val();
        this.updateTextContainer(text);
    }
    
    uploadActiveWord(word) {
        this.debug("Upload word: " + word)
    }
    
    startRecording() {
        this.emit("record-start");
    }
    
    stopRecording() {
        this.emit("record-stop");
    }
    
    deleteCurrentRecord() {
        this.emit("record-delete");
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
    
    scrollToActiveWord() {
        var $el = this.getActiveWordEl();
        
        if (!$el.length) {
            return;
        }
        
        $el.clearQueue();
        $el.stop();
        
        var offsetTop = $el.offset().top - this.$textContainer.offset().top,
            scrollTop = this.$textContainer.scrollTop(),
            height = this.$textContainer.height();
            
        if ((offsetTop > height - 30) || (offsetTop < 5)) {
            this.$textContainer.animate({scrollTop: scrollTop + offsetTop - 3}, 500);
        }
    }
    
    render() {
        this.hideOverlay();
    }
}

$(function () {
    var view = new LearnView();
});
