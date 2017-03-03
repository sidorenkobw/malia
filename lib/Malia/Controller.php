<?php

class Malia_Controller
{
    public $cfg;
    
    protected $_tpl;
    protected $_layoutTpl;
    protected $_noRender = false;
    
    public $view;

    public function __construct($cfg)
    {
        $this->setConfig($cfg);
        $this->_init();
    }
    
    protected function _init()
    {
        $this->initView();
        $this->init();
    }
    
    public function init()
    {}
    
    public function setConfig(array $cfg)
    {
        $this->cfg = $cfg;
    }
    
    public function initView()
    {
        $view = new Malia_View($this->_tpl);
        $view->cfg = $this->cfg;
        
        if ($this->_layoutTpl) {
            $layout = new Malia_View_Layout($this->_layoutTpl);
            $layout->cfg = $this->cfg;
            $view->setLayout($layout);
        }
        
        $this->setView($view);
    }
    
    public function setView(Malia_View $view)
    {
        $this->view = $view;
        return $this;
    }
    
    public function render()
    {
        $this->action();
        
        if (!$this->_noRender) {
            echo $this->view->render();
        }
    }
}
