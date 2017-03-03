<?php

class Malia_View
{
    protected $_vars = array();
    protected $_template;
    protected $_layout;
    
    public function __construct($template, $layout = null)
    {
        $this->setTemplate($template);
        
        if ($layout) {
            $this->setLayout($layout);
        }
    }
    
    public function setTemplate($template)
    {
        $this->_template = $template;
        return $this;
    }
    
    public function getTemplate()
    {
        return $this->_template;
    }
    
    public function setLayout(Malia_View_Layout $layout)
    {
        $this->_layout = $layout;
        return $this;
    }
    
    public function getLayout()
    {
        return $this->_layout;
    }
    
    public function __get($name)
    {
        return isset($this->$name) ? $this->$name : null;
    }
    
    public function __set($name, $val)
    {
        $this->$name = $val;
    }
    
    public function __isset($name)
    {
        return isset($this->$name);
    }
    
    public function __unset($name)
    {
        unset($this->$name);
    }
    
    public function escape($val)
    {
        return htmlspecialchars($val);
    }
    
    public function render()
    {
        ob_start();
        
        require(APP_DIR . '/' . $this->_template);
        
        $output = ob_get_contents();
        ob_end_clean();
        
        if ($this->_layout) {
            $this->_layout->contents = $output;
            $output = $this->_layout->render();
        }
        
        return $output;
    }
}
