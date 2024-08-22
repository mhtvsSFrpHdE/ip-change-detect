cd /d %~dp0
cd server
start "ipcd-srv" /min run.bat
cd ..\client
start "ipcd-client" /min run.bat
