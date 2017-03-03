<?php

require($_SERVER['DOCUMENT_ROOT'] . '/../common.inc.php');
require_once(APP_DIR . '/index/controller/IndexController.php');

$controller = new IndexController($cfg);
$controller->render();
