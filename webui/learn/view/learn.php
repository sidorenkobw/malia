<?php

$this->getLayout()->body_scripts .= '<script src="/lib/bootstrap-notify/js/bootstrap-notify.js?build=' . $this->cfg['build'] . '"></script>';
$this->getLayout()->head_css .= '<link href="/lib/bootstrap-notify/css/bootstrap-notify.css?build=' . $this->cfg['build'] . '" rel="stylesheet">';

$this->getLayout()->body_scripts .= '<script src="/js/learn.js?build=' . $this->cfg['build'] . '"></script>';

$this->getLayout()->js_init .= 'var app = new LearnView(malia);';

?>

<div class="notifications top-right"></div>

<div id="learnApp">
    <div class="learnTextPanel">
        <div class="auth alert alert-danger clearfix" role="alert">
            <div id="firebaseui-auth-container" class="pull-right"></div>
            <span class="glyphicon glyphicon-warning-sign"></span> <strong>Warning!</strong> Learning is in demo mode. Audio recording 
                is disabled for demonstration purpose. Please sign in to start actual learning.
        </div>
        
        <div id="learnTextContainer" class="textPanel"></div>
        <textarea id="learnTextEditor" class="textPanel hidden"></textarea>
    </div>

    <div>Incoming sound meter: <span id="meter"></span></div>

    <div class="controlsPanel">
        <div class="row">
            <div class="col-xs-4">
                <button id="btnLearnRetry" class="btn-learn-retry btn btn-danger btn-lg" tabindex="3" disabled="disabled" title="Cancel current word record and try again. Keys: Backspace">
                    <span class="glyphicon glyphicon-repeat" aria-hidden="true"></span> <span class="caption hidden-xs">Retry Word</span>
                </button>
            </div>
            <div class="col-xs-4" style="text-align: center">
                <button id="btnLearnToggleRecording" class="btn btn-primary btn-lg" tabindex="1" title="Start/stop recording process. Keys: Ctrl + Enter to enter mode, Esc - to exit mode">
                    <span class="glyphicon glyphicon-ice-lolly" aria-hidden="true"></span> <span class="caption hidden-xs">Start Recording</span>
                </button>
            </div>
            <div class="col-xs-4">
                <button id="btnLearnNext" class="btn btn-success btn-lg pull-right" tabindex="2" disabled="disabled" title="Save current word and record the next one. Keys: Space or Enter">
                    <span class="caption hidden-xs">Next Word</span> <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>
                </button>
            </div>
        </div>
        
        <div class="row">
            <div class="col-xs-4" style="text-align: center">
                <button id="btnFullScreen" class="btn btn-default btn-lg" tabindex="4" title="Switch to read mode. Keys: Alt + Enter to enter or exit fullscreen mode">
                    <span class="glyphicon glyphicon-fullscreen" aria-hidden="true"></span> <span class="caption hidden-xs">Full Screen</span>
                </button>
            </div>
            <div class="col-xs-4" style="text-align: center">
                <button id="btnLearnToggleEdit" class="btn btn-default btn-lg" tabindex="4" title="Modify current text. Keys: Esc - to exit edit mode">
                    <span class="glyphicon glyphicon-edit" aria-hidden="true"></span> <span class="caption hidden-xs">Edit Text</span>
                </button>
            </div>
            <div class="col-xs-4" style="text-align: center">
                <button id="btnSkipWord" class="btn btn-default btn-lg" tabindex="4" disabled="disabled" title="Modify current text. Keys: Esc - to exit edit mode">
                    <span class="caption hidden-xs">Skip Word</span> <span class="glyphicon glyphicon-fast-forward" aria-hidden="true"></span>
                </button>
            </div>
        </div>
    </div>
</div>

<div class="overlayContainer">
    <div class="overlay"></div>
    <div class="overlayText">Loading...</div>
</div>
