class LearnView {
    
    constructor() {
        this.isEditMode = false;
        
        this.initEls();
        this.initEditor();
        this.initButtons();
        this.initKeyboardEvents();
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
            .hide();
    }
    
    initKeyboardEvents() {
        $(document).on("keydown", this.onKeyPressed.bind(this));
    }
    
    initButtons() {
        this.$btnToggleEdit.click(this.onClickToggleEdit.bind(this));
    }
    
    onKeyPressed(e) {
        if (e.which == 27) {
            if (this.isEditMode) {
                this.setEditMode(false);
            }
        }
    }
    
    setEditMode(flag) {
        this.isEditMode = !!flag;
        this.onChangeMode();
    }
    
    onChangeMode() {
        if (this.isEditMode) {
            this.$textContainer.hide();
            this.$textEditor.show();
            this.$btnToggleEdit.find("span").eq(0).text("Finished Editing");
            this.$btnToggleRecording.prop("disabled", true);
            this.$btnRetry.prop("disabled", true);
            this.$btnNext.prop("disabled", true);
            this.$textEditor.focus();
        } else {
            this.$textContainer.show();
            this.$textEditor.hide();
            this.$btnToggleEdit.find("span").eq(0).text("Edit Text");
            this.$btnToggleRecording.prop("disabled", false);
            this.$btnRetry.prop("disabled", false);
            this.$btnNext.prop("disabled", false);
        }
    }
    
    onClickToggleEdit(e) {
        this.setEditMode(!this.isEditMode);
    }
    
}

$(function () {
    var view = new LearnView();
});
