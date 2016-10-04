This toolkit helps you to read and properties of your [Rocket R60V](http://www.rocket-espresso.it/r-60v.html)!

In this first state you can use the command line interface (CLI) and the python3 class. The next step will be some more CLI commands and a little WebApp. I am open for more suggestions!

Have a lot of fun...

----

# Requirements
* repo: `git clone https://github.com/JulianKahnert/RocketAPI.git`
* Python: `sudo pip install bottle` 
* linux network interface `wlan0` must be conntected to "RocketEspresso" WLAN

# Workflow
### CLI
* Turn machine on: `python3 R60V.py -on`
* Turn machine off: `python3 R60V.py -off`

### python3 console
```python
from R60V import state

# create object and connect to machine
obj = state()

# show properties
obj.coffeeTemperature
obj.steamTemperature

# turn service boiler off
obj.isServiceBoilerOn = False
# turn machine off
obj.isMachineInStandby = True

# turn service boiler on
obj.isServiceBoilerOn = True
# turn machine on
obj.isMachineInStandby = False

# delete obj to close the connection
del obj
```

# ToDo
* more tools in CLI
* WebApp `RocketGUI.py`

# Unit Testing
* Build Status: [![Build Status](https://travis-ci.org/JulianKahnert/RocketAPI.svg?branch=master)](https://travis-ci.org/JulianKahnert/RocketAPI)
* `python3 -m unittest unit_tests/*.py`

# Acknowledgment
Special thanks to [Jeffrey Stanton](https://github.com/jffry/) for [reverse engineering](https://github.com/jffry/rocket-r60v/blob/master/doc/Reverse%20Engineering.md) and documenting the [protocol](https://github.com/jffry/rocket-r60v/blob/master/doc/Protocol.md)!