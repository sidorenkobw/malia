<?php

class LearnController extends Malia_Controller
{
    protected $_tpl = 'learn/view/learn.php';
    protected $_layoutTpl = 'default/layout.php';
    
    public function init()
    {
        $this->view->getLayout()->currentModule = 'learn';
    }
    
    public function action()
    {
        
    }
}
