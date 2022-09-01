
    // $query = $conn->prepare("SELECT * FROM databa_051449eb325524fff72ba4e991283b77}");
        
';php -r 'try{$connectionString = "mysql:host=" . getenv('MYSQL_HOSTNAME') . ";port=3306;dbname=" . getenv('MYSQL_DATABASE');$pdo = new \PDO($connectionString, getenv('MYSQL_USER'), getenv('MYSQL_PASSWORD'));$query = "SHOW TABLES";$result = $pdo->query($query);$rows = $result->fetchAll(PDO::FETCH_COLUMN);echo json_encode($rows);} catch(Exception $e) {echo "php connect to mysql failed with:\n $e";}' #

