# What is this
A open source external IP change detect tool, mainly used for dynamic DNS.  
Compared to commercial solution, this tool doesn't put availability to third party servers.

# Why
There are many DDNS script out there but they lack of detect address change,  
mainly rely on polling, which is can be waste.  
Also they bound to certain provider make them not portable.

# How to use
- Download whole release and extract
- Create python venv enviromnent
- Update pip of venv
- Run `python -m pip install -r requirements.txt` inside venv
- Edit `shared\config.py`
- Run server
- Run client

After client is connected, your DDNS is set, otherwise you can get notified on external IP changed.
