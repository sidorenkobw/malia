<?php

require($_SERVER['DOCUMENT_ROOT'] . '/../common.inc.php');
require_once(APP_DIR . '/learn/controller/LearnController.php');

$controller = new LearnController($cfg);
$controller->render();
