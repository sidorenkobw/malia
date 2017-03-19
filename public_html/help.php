<?php

require($_SERVER['DOCUMENT_ROOT'] . '/../common.inc.php');
require_once(APP_DIR . '/help/controller/HelpController.php');

$controller = new HelpController($cfg);
$controller->render();
