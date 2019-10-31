<?php
namespace stranger;

class Input
{
    public static function receive()
    {
        if (empty($_POST['phrase'])) {
            return false;
        }

        if ($error = self::badInput($_POST['phrase'])) {
            return $error;
        }

        $phrase = self::clean($_POST['phrase']);

        require_once __DIR__.DIRECTORY_SEPARATOR.'Database.php';
        $pdo = Database::getDatabase();

	if ($phrase == 'clear') {
	    $pdo->prepare("DELETE FROM  phrases WHERE 1")->execute();
	} else {
    	    $pdo->prepare("INSERT INTO phrases (phrase) VALUES (?)")->execute([$phrase]);
	}

        return true;
    }

    public static function badInput($input)
    {
        if (strlen($input) > 40) {
            return 'keep it pithy, dingus';
        }

        if (preg_match('/\d/', $input)) {
            return 'no numbers, jerkwad';
        }

        return false;
    }

    public static function clean($input)
    {
        $input = strtolower($input);
        $input = preg_replace("/[^a-z ]/", ' ', $input);
        $input = preg_replace('!\s+!', ' ', $input);

        return $input;
    }
}
