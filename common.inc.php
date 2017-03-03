<?php

defined('ROOT_DIR') || define('ROOT_DIR', realpath(dirname($_SERVER['DOCUMENT_ROOT'])));
defined('PUBLIC_DIR') || define('PUBLIC_DIR', ROOT_DIR . '/public_html');
defined('APP_DIR') || define('APP_DIR', ROOT_DIR . '/app');
defined('LIB_DIR') || define('LIB_DIR', ROOT_DIR . '/lib');
defined('CFG_DIR') || define('CFG_DIR', APP_DIR . '/config');

spl_autoload_register(function ($class_name) {
    $path = join('/', explode('_', $class_name));
    require_once(LIB_DIR . '/' . $path . '.php');
});

require(CFG_DIR . '/development.php');
