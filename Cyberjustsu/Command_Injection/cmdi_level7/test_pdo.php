<?php

try{
    $connectionString = "mysql:host=" . getenv('MYSQL_HOSTNAME') . ";port=3306;dbname=" . getenv('MYSQL_DATABASE');
    $pdo = new \PDO($connectionString, getenv('MYSQL_USER'), getenv('MYSQL_PASSWORD'));
    echo "Looking good, php connect to mysql successfully.";    
} catch(PDOException $e) {
    echo "php connect to mysql failed with:\n $e";
}

?>