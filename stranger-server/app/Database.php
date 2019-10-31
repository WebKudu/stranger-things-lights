<?php
namespace stranger;

class Database
{
    static $host = '127.0.0.1';
    static $db   = 'stranger';
    static $user = 'stranger';
    static $pass = 'danger';
    static $charset = 'utf8mb4';

    public static function getDatabase(): \PDO
    {
        $dsn = 'mysql:host='.self::$host.';dbname='.self::$db.';charset='.self::$charset;
        $options = [
            \PDO::ATTR_ERRMODE            => \PDO::ERRMODE_EXCEPTION,
            \PDO::ATTR_DEFAULT_FETCH_MODE => \PDO::FETCH_ASSOC,
            \PDO::ATTR_EMULATE_PREPARES   => false,
        ];

        try {
            return new \PDO($dsn, self::$user, self::$pass, $options);
        } catch (\PDOException $e) {
            throw new \PDOException($e->getMessage(), (int)$e->getCode());
        }
    }
}
