cd /d %~dp0
cd server
start /min run.bat
start /min run6.bat
cd ..\client
start /min run.bat
start /min run6.bat