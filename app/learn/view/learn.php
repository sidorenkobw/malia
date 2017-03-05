<?php

$this->getLayout()->body_scripts .= '<script src="/js/learn.js?build=' . $this->cfg['build'] . '"></script>';

?>

<div class="page-header">
    <h1>Learn</h1>
</div>

<div id="learnApp">
    <div class="learnTextPanel">
        <div id="learnTextContainer" class="textPanel"></div>
        <textarea id="learnTextEditor" class="textPanel hidden"></textarea>
    </div>

    <div class="controlsPanel">
        <div class="row">
            <div class="col-md-4 col-sm-4">
                <button id="btnLearnRetry" class="btn-learn-retry btn btn-danger btn-lg">Retry Word <span class="glyphicon glyphicon-repeat" aria-hidden="true"></span></button>
            </div>
            <div class="col-md-4 col-sm-4" style="text-align: center">
                <button id="btnLearnToggleRecording" class="btn btn-primary btn-lg"><span>Start Recording</span> <span class="glyphicon glyphicon-ice-lolly" aria-hidden="true"></span></button>
            </div>
            <div class="col-md-4 col-sm-4">
                <button id="btnLearnNext" class="btn btn-success btn-lg pull-right" style="margin-left: 10px">Next Word <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span></button>
                
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-12" style="text-align: center">
                <button id="btnLearnToggleEdit" class="btn btn-lg"><span>Edit Text</span> <span class="glyphicon glyphicon-edit" aria-hidden="true"></span></button>
            </div>
        </div>
    </div>
    
    <div class="overlayContainer">
        <div class="overlay"></div>
        <div class="overlayText">Loading...</div>
    </div>
</div>
