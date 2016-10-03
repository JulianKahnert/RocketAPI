# Todo

* 

# Requirements
* Python: `sudo pip install bottle` 
* linux interface `wlan0` must be conntected to "RocketEspresso" WLAN

# Webserver
```
python3 RocketGUI.py

@hourly		cd /PATH/TO/RocketAPI/ && git reset --hard develop && git pull --rebase --stat origin develop
```

# Unit Testing
```
python3 -m unittest unit_tests/*.py
```

[![Build Status](https://travis-ci.org/JulianKahnert/RocketAPI.svg?branch=develop)](https://travis-ci.org/JulianKahnert/RocketAPI)