<?php 
if(isset($_GET["debug"])){
    die(show_source(__FILE__));
}
?>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>BizCard Generator</title>
    <link rel=stylesheet href=style.css>
</head>
<body>
    <div class="column">
        <h1>Business card generator!</h1>
        <i style="color:gray; font-size:0.5em">Fun fact: CyberJutsu vẫn chưa có business card nào :D</i>
        <a href="?debug"><pre>Click to view source code </pre></a>
        <img src='demo.png' width=200 height=200 />
    </div>
    <div class="column">
        <form method=get action="index.php">
            <div class="resp-textbox">
            <input type=text name=username placeholder="Enter your username here" />
            <fieldset style="text-align: left">
                <legend>Chọn kiểu bizcard nhé:</legend>
                <input type="radio" name="type" value="eyes"><label>eyes</label><br>
                <input type="radio" name="type" value="turtle"><label>turtle</label><br>
                <input type="radio" name="type" value="dragon"><label>dragon</label><br>
                <input type="radio" name="type" value="figlet"><label>figlet</label><br>
                <input type="radio" name="type" value="toilet"><label>toilet</label><br>
                <input type="radio" name="type" value="inception"><label>inception</label><br>
                <input type="radio" name="type" value="tenet"><label>tenet</label><br>
                <input type="radio" name="type" value="gnu"><label>gnu</label><br>
                <input type="radio" name="type" value="elephant"><label>elephant</label><br>
                <input type="radio" name="type" value="random" checked><label>random</label><br>
            </fieldset>
            <input type=submit value="Generate for free!">
            </div>
        </form>
        ------------------ 


<?php
// Challenge starts here

function validate_username($input){
    // <START>
    // ... your code here
    // </START>
    return $input;
}

function normalize($input) {
    $input = addslashes($input);
    $input = urldecode($input);
    return $input;
}

$type           = $_GET['type'];
$raw_username   = $_GET['username'];
$username       = validate_username($raw_username);
$username       = normalize($username);

echo "<pre>"; // tag này giúp in ra font monospace để có thể biểu diễn ascii art
echo "[DEBUG] Username: $username\n";


// Tùy vào type mà ta sẽ in ra ASCII art khác nhau. tuyệt vời

switch($type){
    case 'eyes':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -f eyes -n 
        EOF;
        break;
    case 'turtle':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -f turtle -n 
        EOF;
        break;
    case 'dragon':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -f dragon -n 
        EOF;
        break;   
    case 'figlet':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -n ; figlet "Hello $username"
        EOF;
        break;
    case 'toilet':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -n ; toilet 'Hello $username'
        EOF;
        break;  
    case 'inception':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -n | cowthink -n
        EOF;
        break; 
    case 'tenet':
        $cowsay = <<<EOF
        echo 'Hello $username' | cowsay -n | cowthink -n | cowsay -n 
        EOF;
        break;
    case 'gnu':
        $cowsay = <<<EOF
        cowsay -f gnu $raw_username
        EOF;
        break;
    case 'random':
    default:
        $cowsay = <<<EOF
        fortune | cowsay -n | cowthink -n
        EOF;
}
echo "[DEBUG] Command: $cowsay\n\n\n";

function safe_exec($cmd) {
    // setup stdin, stdout, stderr
    $descriptors = array(
        0 => array('pipe', 'r'), 
        1 => array('pipe', 'w'), 
        2 => array('pipe', 'w')
    );
    
    /*
        Command may be passed as array of command parameters. In this case, 
        the process will be opened directly (without going through a shell)
        and PHP will take care of any necessary argument escaping.
        Refs: https://www.php.net/manual/en/function.proc-open.php
    */
    $cmd = explode(" ", $cmd);
    $proc = proc_open($cmd, $descriptors, $pipes);
    echo stream_get_contents($pipes[1]);
    echo stream_get_contents($pipes[2]);
    proc_close($proc);
}

if ($type == 'gnu') {
    safe_exec($cowsay);
} else {
    passthru($cowsay);
}
echo "</pre>";

?>
    </div>
</body>

</html>