<!DOCTYPE html>
<html lang="en">
<head>
    <?php echo $this->head_start ?>
    
    <?php echo $this->head_before_meta ?>
    
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <?php echo $this->head_after_meta ?>
    
    <title><?php echo strlen($this->title) ? $this->title : 'Malia Speech' ?></title>

    <?php echo $this->head_before_css ?>
    
    <!-- Bootstrap -->
    <link href="<?php echo $this->cfg['libs']['bootsrap_css'] ?>" rel="stylesheet">
    <link href="/css/jumbotron-narrow.css" rel="stylesheet">
    <link href="/css/malia.css?build=<?php echo $this->cfg['build'] ?>" rel="stylesheet">
    
    <?php echo $this->head_css ?>
    
    <?php echo $this->head_after_css ?>
    
    <?php echo $this->head_before_scripts ?>
    
    <?php echo $this->head_scripts ?>
    
    <?php echo $this->head_after_scripts ?>
    
    <?php echo $this->head_end ?>
</head>
<body>

<?php echo $this->body_start ?>

<?php
$menu = array(
    'home' => array('title' => 'Home', 'url' => '/'),
    'login' => array('title' => 'Login', 'url' => '#login'),
    'learn' => array('title' => 'Learn', 'url' => '/learn.php'),
    'about' => array('title' => 'About', 'url' => '#about'),
    'contact' => array('title' => 'Contact', 'url' => '#contact')
);
?>

<div class="container">
    <div class="header clearfix">
        <nav>
            <ul class="nav nav-pills pull-right">
                <?php foreach ($menu as $module => $item): ?>
                    <li role="presentation"<?php echo ($module == $this->currentModule ? ' class="active"' : '') ?>>
                        <a href="<?php echo $this->escape($item['url']) ?>"><?php echo $this->escape($item['title']) ?></a>
                    </li>
                <?php endforeach; ?>
            </ul>
        </nav>
        
        <h3 class="text-muted">Malia Speech</h3>
    </div>

    <?php echo $this->contents ?>

    <footer class="footer">
        <p>&copy; 2017 Malia Speech</p>
    </footer>

</div> <!-- /container -->


<?php echo $this->body_before_scripts ?>

<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
<script src="<?php echo $this->cfg['libs']['jquery'] ?>"></script>

<!-- Include all compiled plugins (below), or include individual files as needed -->
<script src="<?php echo $this->cfg['libs']['bootsrap_js'] ?>"></script>

<?php echo $this->body_scripts ?>

<?php echo $this->body_after_scripts ?>

<?php echo $this->body_end ?>

</body>
</html>
