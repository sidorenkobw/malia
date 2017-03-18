<?php

require($_SERVER['DOCUMENT_ROOT'] . '/../common.inc.php');
require_once(APP_DIR . '/speak/controller/SpeakController.php');

$controller = new SpeakController($cfg);
$controller->render();
