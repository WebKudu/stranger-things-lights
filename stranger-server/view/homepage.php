<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>A Nightmare on Edwards Street 2</title>
    <link rel="stylesheet" type="text/css" href="/css/main.css?v=<?php echo filemtime(__DIR__.DIRECTORY_SEPARATOR.'..'.DIRECTORY_SEPARATOR.'www'.DIRECTORY_SEPARATOR.'css'.DIRECTORY_SEPARATOR.'main.css'); ?>" />
</head>
<body>
    <video autoplay muted loop id="horrorscope">
        <source src="/assets/Horrorscope-Medium-Res.mp4" type="video/mp4">
    </video>
    <form method="POST">
        <input type="text" name="phrase" autocomplete="off" />
        <input type="submit" value="I'M FEELING UNLUCKY!" />
    </form>
    <?php if (!empty($error) && is_string($error)) { ?>
        <div class="error"><?php echo $error; ?></div>
    <?php } ?>
</body>
</html>
