<?php

$cfg['version'] = 0.1;
$cfg['build'] = 20;

// Warning. This section is exposed to js:
$cfg['auth']['federated']['firebase'] = array(
    'apiKey' => "AIzaSyAmTywORdeldcyolqVUnj_gUEyzBlwRP3U",
    'authDomain' => "malia-speech.firebaseapp.com",
    'databaseURL' => "https://malia-speech.firebaseio.com",
    'storageBucket' => "malia-speech.appspot.com",
    'messagingSenderId' => "808979079469"
);

$cfg['libs']['bootstrap_js'] = '/lib/bootstrap/3.3.7/js/bootstrap.min.js';
$cfg['libs']['bootstrap_css'] = '/lib/bootstrap/3.3.7/css/bootstrap.min.css';
$cfg['libs']['jquery'] = '/lib/jquery/jquery-3.1.1.min.js';
$cfg['libs']['requirejs'] = '/lib/requirejs/require-2.3.3.min.js';
