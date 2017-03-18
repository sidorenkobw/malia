define([
    "malia",
    "view",
    "recorder",
    "bootstrapnotify"
], function (
    malia,
    View,
    Recorder,
    BootstrapNotify
) {
    class LearnView extends View {
        constructor(malia) {
            super();

            this.cfg = malia.cfg || {};

            /* idle|record|edit */
            this.mode = "idle";
            this.activeWordIndex = 0;
            this.$words = null;
            this.isFullscreen = false;
            this.isFullscreenAuto = false;
            this.recordTimeout = 10000;
            this.recordTimer = null;
            this.uploadedWordsCounter = 0;

            this.initEls();

            if (malia.debugLog) {
                this.setDebugLog(malia.debugLog);
            }

            if (location.protocol != "https:") {
                var url = location.href.replace(/^http\:/, "https\:");
                this.error('HTTP protocol is not supported. Please open using HTTPS: <a href="'+url+'">'+url+'</a>');
                return;
            }

            this.auth = malia.auth;
            if (!this.auth) {
                this.debug("No auth view", "log", "LearnView");
                this.error('Internal error: unable to perform authentication.');
                return;
            }

            this.initRecorder();
            this.initEvents();
            this.initButtons();
            this.initKeyboardEvents();
            this.initEditor();
            this.initTextContainer();
        }

        initRecorder() {
            this.recorder = new Recorder(document.querySelector("#meter"),
                this.render.bind(this), this.error.bind(this));

            this.recorder.setDebugLog(this.debugLog);
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
                "active-word": this.onActiveWord
            };

            for (var event in events) {
                this.on(event, events[event].bind(this));
            }
        }

        initEls() {
            this.$app = $("#learnApp");
            this.$textContainer = $("#textContainer");
            this.$textEditor = $("#textEditor");
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
            this.$textEditor
                .removeClass("hidden")
                .hide();

            this.updateText(this.loadTextFromStorage());
            this.emit("mode");
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

        getStorage() {
            return this.auth.getProxy();
        }

        skipActiveWord() {
            this.emit("word-skip");

            if (this.mode == "record") {
                this.cancelRecording();
            }

            this.setActiveWord(this.activeWordIndex + 1);
        }

        switchActiveWord(i) {
            if (this.mode == "record") {
                this.cancelRecording();
            }

            this.setActiveWord(i);
        }

        _setActiveWord(i) {
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

        setActiveWord(i) {
            // Change active word only after recording is stopped
            if (this.recorder.isRecording()) {
                this.recorder.once("stop", (() => { this._setActiveWord(i) }).bind(this));
            } else {
                this._setActiveWord(i);
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
                this.setFullScreenbyUser(!this.isFullscreen);
            } else if (e.which == 32 || e.which == 13) {
                // space or enter
                if (this.mode == "record") {
                    e.preventDefault();
                    this.emit("word-next");
                }
            } else if (e.which == 8) {
                // backspace
                if (this.mode == "record") {
                    e.preventDefault();
                    this.emit("word-retry");
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
            this.setFullScreenbyUser(!this.isFullscreen);
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
            this.debug("Mode idle on", "log", "LearnView_ModeChange");
        }

        onModeIdleOff() {
            this.debug("Mode idle off", "log", "LearnView_ModeChange");
        }

        onModeRecordOn() {
            this.debug("Mode record on", "log", "LearnView_ModeChange");

            this.uploadedWordsCounter = 0;
            this.updateUploadedWords();

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

            if (!this.isFullscreen) {
                this.isFullscreenAuto = true;
            }
            this.setFullscreen(true);

            this.startRecording();
        }

        onModeRecordOff() {
            this.debug("Mode record off", "log", "LearnView_ModeChange");

            this.$btnToggleRecording
                .addClass("btn-primary")
                .removeClass("btn-danger")
                .find(".caption")
                .eq(0)
                .text("Start Recording");

            this.$btnRetry.prop("disabled", true);
            this.$btnNext.prop("disabled", true);
            this.$btnSkip.prop("disabled", true);

            if (this.isFullscreenAuto) {
                this.setFullscreen(false);
            }

            this.cancelRecording();
        }

        onModeEditOn() {
            this.debug("Mode edit on", "log", "LearnView_ModeChange");

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
            this.debug("Mode edit off", "log", "LearnView_ModeChange");

            this.$textEditor.hide();
            this.$textContainer.show();

            this.$btnToggleEdit
                .toggleClass("btn-warning", false)
                .find(".caption")
                .eq(0)
                .text("Edit Text");

            this.showOverlay("Analyzing text...");

            setTimeout((function () {
                this.updateText();
                this.hideOverlay();
            }).bind(this), 10);
        }

        setFullscreen(flag) {
            this.isFullscreen = !!flag;
            this.emit("fullscreen-" + (this.isFullscreen ? "on" : "off"));
        }

        setFullScreenbyUser(flag) {
            this.isFullscreenAuto = false;
            this.setFullscreen(flag);
        }

        onFullscreenOn() {
            this.debug("Fullscreen on", "log", "LearnView");

            this.$app.addClass("fullscreen");
            this.$btnToggleFullscreen.addClass("btnChecked");
        }

        onFullscreenOff() {
            this.debug("Fullscreen off", "log", "LearnView");

            this.$app.removeClass("fullscreen");
            this.$btnToggleFullscreen.removeClass("btnChecked");
        }

        onActiveWord() {
            this.debug("Active word changed", "log", "LearnView");
            this.$words.removeClass("active");
            this.getActiveWordEl().addClass("active");
            this.scrollToActiveWord();
        }

        onWordNext() {
            this.stopRecording();
            this.setActiveWord(this.activeWordIndex+1);
        }

        onWordRetry() {
            this.debug("Retry word", "log", "LearnView");

            this.cancelRecording((function () {
                this.startRecording();
            }).bind(this));
        }

        onWordSkip() {
            this.debug("Skip word", "log", "LearnView");
        }

        getActiveWordEl() {
            return this.$words.eq(this.activeWordIndex);
        }

        saveTextToStorage(text) {
            localStorage.setItem("text", text);
        }

        loadTextFromStorage() {
            return localStorage.getItem("text") || "";
        }

        deleteTextFromStorage() {
            localStorage.removeItem("text");
        }

        updateText(text) {
            var text = arguments.length ? text : this.$textEditor.val(),
                saveText = !arguments.length;

            if (text.trim() == "") {
                text = "Click \"Edit Text\" to add your text.";
                saveText = false;
                this.$textEditor.val(text);
            }

            if (arguments.length) {
                this.$textEditor.val(text);
            }

            if (saveText) {
                this.saveTextToStorage(text);
            }

            var textHtml = this.textToHtml(text);
            this.$textContainer.html(textHtml);

            this.$textContainer
                .empty()
                .html(textHtml);

            this.$words = this.$textContainer.find("span");
            this.setActiveWord(0);
        }

        uploadWord(word, record) {
            // TODO handle cancel case
            var user = this.auth.getUser();

            if (user.getRole() != "authenticated") {
                this.showNotification("danger", "Guests are not allowed to save recordings. Record was not saved.");
                return;
            }

            this.debug("Upload started. Word: " + word, "log", "LearnView_Upload");

            //TODO sync with words db:
            var path = "incoming/" + this.auth.getUser().getId() + "/" + escape(word) + "/" + Date.now() + ".webm";

            this.debug("Upload path: " + path, "log", "LearnView_Upload");

            if (!record) {
                this.showNotification("danger", "Word was not uploaded");
                this.debug("Error: Record is empty", "log", "LearnView_Upload");
                return;
            }

            this.debug(record, "log", "LearnView_Upload_Start");

            this.getStorage().upload(record, path).then((function(snapshot) {
                this.debug("Done uploading of word: " + word + "to storage path: " + path, "log", "LearnView_Upload");
                this.uploadedWordsCounter++;
                this.updateUploadedWords();
            }).bind(this));
        }

        updateUploadedWords() {
            $(".uploadedWordsCounter").text(this.uploadedWordsCounter);
        }

        startRecording() {
            var word = this.getActiveWordEl().text().toLowerCase();
            if (!word || word == "") {
                this.recorder.cancelRecording();
                this.showNotification("Danger", "Error: empty word");
                return;
            }

            this.once("audio-ready", function (record) {
                this.uploadWord(word, record);
            }.bind(this));

            this.recorder.startRecording();
            this.debug("Start recording word: " + word, "log", "LearnView");

            this.scrollToActiveWord();
            this.recordTimer = setTimeout((function () {
                this.setMode("idle");
                this.showNotification("danger", "Recording timeout");
            }).bind(this), this.recordTimeout);
        }

        stopRecording() {
            this.recorder.once("data-ready", function (blob) {
                this.emit("audio-ready", blob);
            }.bind(this));

            this.recorder.stopRecording();
            this.debug("Stop recording", "log", "LearnView");
            clearTimeout(this.recordTimer);
        }

        cancelRecording(callback) {
            this.off("audio-ready");
            this.recorder.stopRecording(callback);
            this.debug("Cancel recording", "log", "LearnView");
            clearTimeout(this.recordTimer);
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

        error(msg, err) {
            var div = $("<div>")
                .addClass("alert alert-danger")
                .html(msg);

            this.$app.html(div);
            this.hideOverlay();
        }

        render() {
            this.hideOverlay();
        }
    }

    return LearnView;
});
