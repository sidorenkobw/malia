<?php

$this->getLayout()->head_css .= '<link href="/lib/bootstrap-notify/css/bootstrap-notify.css?build=' . $this->cfg['build'] . '" rel="stylesheet">';

$this->getLayout()->js_init .= '
require(["malia", "view/speak"], function (malia, SpeakView) {
    var app = new SpeakView(malia);
});
';

?>

<div class="notifications top-right"></div>

<div id="speakApp">
    <div class="flex">
        <div id="textContainer" class="textPanel"></div>
    </div>

    <div style="text-align: center;">Incoming sound meter: <span id="meter"></span></div>

    <div class="controlsPanel">
        <div class="row">
            <div class="col-xs-4 col-xs-offset-4">
                <button id="btnStartRecording" class="btn btn-primary btn-lg" tabindex="1" title="Start/stop recording process. Keys: Ctrl + Enter to enter mode, Esc - to exit mode">
                    <span class="glyphicon glyphicon-ice-lolly" aria-hidden="true"></span> <span class="caption hidden-xs">Start Recording</span>
                </button>
                <button id="btnNextWord" class="btn btn-success btn-lg hidden" tabindex="1">
                    <span class="caption hidden-xs">Next Word</span> <span class="glyphicon glyphicon-step-forward" aria-hidden="true">
                </button>
            </div>
        </div>
    </div>
</div>

<div class="overlayContainer">
    <div class="overlay"></div>
    <div class="overlayText">Loading...</div>
</div>
