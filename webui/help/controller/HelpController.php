<?php

class HelpController extends Malia_Controller
{
    protected $_tpl = 'help/view/help.php';
    protected $_layoutTpl = 'default/layout.php';

    public function init()
    {
        $this->view->getLayout()->currentModule = 'help';
    }

    public function action()
    {

    }
}
