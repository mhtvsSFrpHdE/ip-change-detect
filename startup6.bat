cd /d %~dp0
cd server
start "ipcd-srv6" /min run6.bat
cd ..\client
start "ipcd-client6" /min run6.bat
