<?php

$this->getLayout()->body_scripts .= '<script src="/js/learn.js?build=' . $this->cfg['build'] . '"></script>';

?>

<div class="page-header">
    <h1>Learn</h1>
</div>

<div class="learnTextPanel">
    <div id="learnTextContainer" class="textPanel"></div>
    <textarea id="learnTextEditor" class="textPanel hidden"></textarea>
</div>

<div class="controlsPanel">
    <div class="row">
        <div class="col-md-3">
            <button id="btnLearnRetry" class="btn-learn-retry btn btn-danger btn-lg">Retry Current Word <span class="glyphicon glyphicon-repeat" aria-hidden="true"></span></button>
        </div>
        <div class="col-md-6" style="text-align: center">
            <button id="btnLearnToggleRecording" class="btn btn-primary btn-lg">Start Recording <span class="glyphicon glyphicon-ice-lolly" aria-hidden="true"></span></button>
        </div>
        <div class="col-md-3">
            <button id="btnLearnNext" class="btn btn-success btn-lg" style="margin-left: 10px">Next Word <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span></button>
            
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-6 col-md-offset-3" style="text-align: center">
            <button id="btnLearnToggleEdit" class="btn btn-lg"><span>Edit Text</span> <span class="glyphicon glyphicon-edit" aria-hidden="true"></span></button>
        </div>
    </div>
</div>
