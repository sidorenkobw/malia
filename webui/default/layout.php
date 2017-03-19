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

    <link href="<?php echo $this->cfg['libs']['bootstrap_css'] ?>" rel="stylesheet">
    <link href="/css/malia.css?build=<?php echo $this->cfg['build'] ?>" rel="stylesheet">
    <link href="/lib/bootstrap-notify/css/bootstrap-notify.css?build=<?php echo $this->cfg['build'] ?>" rel="stylesheet">
    <link type="text/css" rel="stylesheet" href="https://cdn.firebase.com/libs/firebaseui/1.0.0/firebaseui.css">

    <?php echo $this->head_css ?>

    <?php echo $this->head_after_css ?>

    <?php echo $this->head_before_scripts ?>

    <script src="https://www.gstatic.com/firebasejs/3.6.10/firebase.js"></script>
    <script src="https://cdn.firebase.com/libs/firebaseui/1.0.0/firebaseui.js"></script>

    <?php echo $this->head_scripts ?>

    <?php echo $this->head_after_scripts ?>

    <?php echo $this->head_end ?>
</head>
<body>

<?php echo $this->body_start ?>

<?php
$menu = array(
    'home' => array('title' => 'Home', 'url' => '/'),
    'learn' => array('title' => 'Learn', 'url' => '/learn.php'),
    'speak' => array('title' => 'Speak', 'url' => '/speak.php'),
    'about' => array('title' => 'About', 'url' => '/about.php'),
    'help' => array('title' => 'Help', 'url' => '/help.php'),
    'contact' => array('title' => 'Contact', 'url' => '#contact')
);
?>

<div class="container">
    <div class="header clearfix">
        <nav class="navbar navbar-default">
            <div class="container-fluid">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>

                    <a class="navbar-brand" href="/">
                        <span class="caption">Malia Speech</span>
                        <span class="icon glyphicon glyphicon-volume-up"></span>
                    </a>
                </div>
                <div id="navbar" class="navbar-collapse collapse pull-right">
                    <ul class="nav navbar-nav nav-pills">
                        <?php foreach ($menu as $module => $item): ?>
                            <li role="presentation"<?php echo ($module == $this->currentModule ? ' class="active"' : '') ?>>
                                <a href="<?php echo $this->escape($item['url']) ?>"><?php echo $this->escape($item['title']) ?></a>
                            </li>
                        <?php endforeach; ?>
                        <li class="btnSignin hidden"><a href="#">Sign In</a></li>
                        <li class="btnSignout hidden"><a href="#">Sign Out</a></li>
                    </ul>
                </div>
            </div>
        </nav>
    </div>

    <div id="firebaseui-auth-container"></div>

    <?php echo $this->contents ?>

    <footer class="footer">
        <p>&copy; 2017 Malia Speech</p>
    </footer>

</div> <!-- /container -->


<?php echo $this->body_before_scripts ?>

<script>
    var malia = {
        cfg : {
            build: <?php echo json_encode($this->cfg['build']); ?>,
            auth: <?php echo json_encode($this->cfg['auth']['federated']); ?>
        },
        callback: function () {
            <?php echo $this->js_init ?>
        }
    };
</script>

<script src="<?php echo $this->cfg['libs']['requirejs'] ?>" data-main="/js/app.js?build=<?php echo $this->cfg['build'] ?>"></script>

<?php echo $this->body_scripts ?>

<?php echo $this->body_after_scripts ?>

<?php echo $this->body_end ?>

</body>
</html>
