Set-ExecutionPolicy Unrestricted;

if($args.Count -eq 1) {
    $scriptPath = ".\$($args[0])\Scripts\Activate.ps1"
    & $scriptPath
}