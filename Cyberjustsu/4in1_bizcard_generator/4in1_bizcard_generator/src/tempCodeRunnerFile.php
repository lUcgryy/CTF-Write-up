<?php
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
    case 'random':
    default:
        $cowsay = <<<EOF
        fortune | cowsay -n | cowthink -n
        EOF;
}