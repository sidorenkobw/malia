<!DOCTYPE html>
<html lang="en">
<head>
    <?php echo $this->head_start ?>
    
    <?php echo $this->head_before_meta ?>
    
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <?php echo $this->head_after_meta ?>
    
    <title><?php echo strlen($this->title) ? $this->title : 'Malia' ?></title>

    <?php echo $this->head_before_css ?>
    
    <!-- Bootstrap -->
    <link href="<?php echo $this->cfg['libs']['bootsrap_css'] ?>" rel="stylesheet">
    
    <?php echo $this->head_css ?>
    
    <?php echo $this->head_after_css ?>
    
    <?php echo $this->head_before_scripts ?>
    
    <?php echo $this->head_scripts ?>
    
    <?php echo $this->head_after_scripts ?>
    
    <?php echo $this->head_end ?>
</head>
<body>
<?php echo $this->body_start ?>

<?php echo $this->contents ?>

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
