<?php

class AboutController extends Malia_Controller
{
    protected $_tpl = 'about/view/about.php';
    protected $_layoutTpl = 'default/layout.php';

    public function init()
    {
        $this->view->getLayout()->currentModule = 'about';
    }

    public function action()
    {

    }
}
