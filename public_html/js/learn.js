class LearnView {
    constructor() {
        /* idle|record|edit */
        this.mode = "idle";
        
        this.initEls();
        this.initButtons();
        this.initKeyboardEvents();
        this.initEditor();
    }
    
    initEls() {
        this.$textContainer = $("#learnTextContainer");
        this.$textEditor = $("#learnTextEditor");
        this.$btnRetry   = $("#btnLearnRetry");
        this.$btnToggleRecording = $("#btnLearnToggleRecording");
        this.$btnNext = $("#btnLearnNext");
        this.$btnToggleEdit = $("#btnLearnToggleEdit");
    }
    
    initEditor() {
        this.$textEditor
            .removeClass("hidden")
            .val(this.loadTextFromStorage())
            .hide();
            
        this.updateText();
        this.onChangeMode();
    }
    
    saveTextToStorage(text) {
        localStorage.setItem("text", text);
    }
    
    loadTextFromStorage() {
        return localStorage.getItem("text");
    }
    
    initKeyboardEvents() {
        $(document).on("keydown", this.onKeyPressed.bind(this));
    }
    
    initButtons() {
        this.$btnToggleEdit.click(this.onClickToggleEdit.bind(this));
        this.$btnToggleRecording.click(this.onClickToggleRecording.bind(this));
        $(document).click((function(e) {
            e.preventDefault();
            if (this.mode == "edit" && e.target !== this.$textEditor.eq(0)) {
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
    
    setMode(mode) {
        var old = this.mode;
        this.mode = mode;
        this.onChangeMode(old);
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
        } else {
            this.$btnToggleEdit.find("span").eq(0).text("Edit Text");
            this.$btnToggleRecording.prop("disabled", false);
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
    
    onChangeMode(old) {
        if (old == "edit") {
            this.updateText();
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
        }
        
        this.updateButtons();
    }
    
    onClickToggleEdit(e) {
        e.stopPropagation();
        this.setMode(this.mode == "edit" ? "idle" : "edit");
    }
    
    onClickToggleRecording(e) {
        this.setMode(this.mode == "record" ? "idle" : "record");
    }
    
    textToHtml(text) {
        text = text
            .split(/([a-zA-Z]+'[a-z]+|[a-zA-Z]+)/)
            .map(function (word) {
                if (word.match(/([a-zA-Z]+'[a-z]+|[a-zA-Z]+)/)) {
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
    }
}

$(function () {
    var view = new LearnView();
});
