<?php

require($_SERVER['DOCUMENT_ROOT'] . '/../common.inc.php');
require_once(APP_DIR . '/about/controller/AboutController.php');

$controller = new AboutController($cfg);
$controller->render();
