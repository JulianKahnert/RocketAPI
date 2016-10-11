This toolkit helps you to read and properties of your [Rocket R60V](http://www.rocket-espresso.it/r-60v.html)!

In this first state you can use the command line interface (CLI) and the Python 3 class. The next step will be some more CLI commands and a little WebApp. I am open for more suggestions!

Have a lot of fun...

----

# Requirements
* repo: `git clone https://github.com/JulianKahnert/RocketAPI.git`
* Python: `pip3 install bottle`
* linux network interface `wlan0` must be connected to "RocketEspresso" WLAN

# Workflow
### CLI
* Turn machine on: `./R60V.py -on`
* Turn machine off: `./R60V.py -off`
* for all CLI commands see: `./R60V.py --help`


### Python 3 console
```python
from R60V import state
obj = state()                       # create object and connect to machine

obj.coffeeTemperature               # show property: coffeeTemperature
obj.steamTemperature                # show property: steamTemperature

obj.isServiceBoilerOn = False       # turn service boiler off
obj.isMachineInStandby = True       # turn machine off

obj.isServiceBoilerOn = True        # turn service boiler on
obj.isMachineInStandby = False      # turn machine on

del obj                             # delete obj to close the connection
```

# Unit Testing
* Build Status: [![Build Status](https://travis-ci.org/JulianKahnert/RocketAPI.svg?branch=master)](https://travis-ci.org/JulianKahnert/RocketAPI)
* `python3 -m unittest unit_tests/*.py`

# Acknowledgment
Special thanks to [Jeffrey Stanton](https://github.com/jffry/) for [reverse engineering](https://github.com/jffry/rocket-r60v/blob/master/doc/Reverse%20Engineering.md) and documenting the [protocol](https://github.com/jffry/rocket-r60v/blob/master/doc/Protocol.md)!

# Known Errors
* sometimes getting write messages (`w004A0001OKA7`) from the R60V