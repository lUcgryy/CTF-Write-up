<?php
    if(isset($_POST['command'],$_POST['target'])){
        $command = $_POST['command'];
        $target = $_POST['target'];
		switch($command) {
			case "ping":
				$result = shell_exec("timeout 10 ping -c 4 '$target' 2>&1");
				break;
			case "nslookup":
				$result = shell_exec("timeout 10 nslookup '$target' 2>&1");
				break;	
			case "dig":
				$result = shell_exec("timeout 10 dig '$target' 2>&1");
				break;
		}
		die($result);
    }
?>