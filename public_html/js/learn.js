class LearnView {
    constructor() {
        this.initEls();
        
        /* idle|record|edit */
        this.mode = "idle";
        this.currentWordIndex = 0;
        this.$words = null;
        
        this.initButtons();
        this.initKeyboardEvents();
        this.initEditor();
        this.initTextContainer();
    }
    
    initEls() {
        this.$textContainer = $("#learnTextContainer");
        this.$textEditor = $("#learnTextEditor");
        this.$btnRetry   = $("#btnLearnRetry");
        this.$btnToggleRecording = $("#btnLearnToggleRecording");
        this.$btnNext = $("#btnLearnNext");
        this.$btnToggleEdit = $("#btnLearnToggleEdit");
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
        }
    }
    
    onChangeMode(old) {
        if (old == "edit") {
            this.updateText();
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
    
    onClickToggleEdit(e) {
        e.stopPropagation();
        this.setMode(this.mode == "edit" ? "idle" : "edit");
    }
    
    onClickToggleRecording(e) {
        this.setMode(this.mode == "record" ? "idle" : "record");
    }
    
    onClickNext(e) {
        this.stopRecording();
        this.uploadCurrentWord(this.$words.eq(this.currentWordIndex).text());
        
        if (this.$words.length == this.currentWordIndex+1) {
            this.setMode("idle");
            this.setActiveWord(0);
        } else {
            this.setActiveWord(this.currentWordIndex+1)
            this.startRecording();
        }
    }
    
    onClickRetry(e) {
        this.stopRecording();
        this.deleteCurrentRecord();
        this.startRecording();
    }

    setMode(mode) {
        var old = this.mode;
        this.mode = mode;
        this.onChangeMode(old);
    }
    
    setActiveWord(index)
    {
        this.currentWordIndex = index;
        this.updateActiveWord();
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
            this.$btnToggleEdit.find("span").eq(0).text("Finish Editing");
            this.$btnToggleRecording.prop("disabled", true);
            this.$btnToggleEdit.toggleClass("btn-primary", true);
        } else {
            this.$btnToggleEdit.find("span").eq(0).text("Edit Text");
            this.$btnToggleEdit.toggleClass("btn-primary", false);
            this.$btnToggleRecording.prop("disabled", !this.$words.length);
        }
        
        if (this.mode == "record") {
            this.$btnToggleRecording.find("span").eq(0).text("Stop Recording");
            this.$btnToggleRecording.removeClass("btn-primary");
            this.$btnToggleRecording.addClass("btn-danger");
            this.$btnRetry.prop("disabled", false);
            this.$btnNext.prop("disabled", false);
        } else {
            this.$btnToggleRecording.find("span").eq(0).text("Start Recording");
            this.$btnToggleRecording.addClass("btn-primary");
            this.$btnToggleRecording.removeClass("btn-danger");
            this.$btnRetry.prop("disabled", true);
            this.$btnNext.prop("disabled", true);
        }
    }
    
    uploadCurrentWord(word) {
        console.log("Upload word: " + word)
    }
    
    startRecording() {
        console.log("Start recording");
    }
    
    stopRecording() {
        console.log("Stop recording");
    }
    
    deleteCurrentRecord()
    {
        console.log("Delete current record");
    }
    
    textToHtml(text) {
        var mask = /([a-zA-Z]+'[a-z]+|[a-zA-Z0-9]+)/;
        text = text
            .split(mask)
            .map(function (word) {
                if (word.match(mask)) {
                    word = "<span>" + $("<span>").text(word).html() + "</span>"
                }
                
                return word;
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
    
    updateActiveWord() {
        this.$words.removeClass("active");
        this.$words.eq(this.currentWordIndex).addClass("active");
    }
}

$(function () {
    var view = new LearnView();
});
