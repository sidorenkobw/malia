<?php

class SpeakController extends Malia_Controller
{
    protected $_tpl = 'speak/view/speak.php';
    protected $_layoutTpl = 'default/layout.php';
    
    public function init()
    {
        $this->view->getLayout()->currentModule = 'speak';
    }
    
    public function action()
    {
        
    }
}
