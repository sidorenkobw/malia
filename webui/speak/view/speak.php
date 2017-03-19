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

    <div id="wave-graph">

    </div>

    <div class="controlsPanel">
        <div class="row">
            <div class="col-xs-4 col-xs-offset-2">
                <button id="btnClearText" class="btn btn-danger btn-lg" disabled="disabled">
                    <span class="glyphicon glyphicon-remove" aria-hidden="true"></span> <span class="caption hidden-xs">Clear Text</span>
                </button>
            </div>
            <div class="col-xs-4">
                <button id="btnStartRecording" class="btn btn-primary btn-lg" tabindex="1">
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
