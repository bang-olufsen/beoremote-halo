# Beoremote Halo

<img src="https://github.com/bang-olufsen/beoremote-halo/blob/main/Docs/Images/Halo%20CI%20silver%20wall.png" width=40% height=40% align="right">



## Welcome
Welcome to the public GitHub page for the Bang & Olufsen Beoremote Halo.
Beoremote Halo gives you all the convenience of a simple user interface to operate your Bang & Olufsen music system. When you get close to Beoremote Halo, the display lights up and offers you a one button press to select your music. There is no need to use your mobile device or to pull anything out of your pocket and fiddle around trying to find the right app to get started. With the Home Automation System API your remote can also be extended to control your Home.
<br />
<br />
You can find out more about Beoremote Halo on the Bang & Olufsen retail website [here](https://www.bang-olufsen.com/en/us/accessories/beoremote-halo):
<br />
<br />
<br />
## TL;DR
The python package `beoremote-halo` contains a python library for communicating to Beoremote Halo and a command line tool for discovering Beoremote Halo on the network.

Install using pip:
```
$ pip3 install beoremote-halo
```
Scan for Beoremote Halo on the network by running in the terminal
```
$ beoremote-halo scan
If Beoremote Halo does not appear on the list, try waking it up while discovery in running.
Press enter to exit...

BeoremoteHalo-XXXXXXXX.local
...
```
To tryout the Home Automation controls on Beoremote Halo run the bundle demo using the discovered Beoremote Halo hostname:
```
$ beoremote-halo demo --hostname BeoremoteHalo-XXXXXXXX.local
```
## Beoremote Halo Home Automation System API
The Home Automation System API is an open source Async API that allows you to interact with a Beoremote Halo from a control system.
Using a websocket to communicate with the Beoremote Halo, it is possible to create a configuration of buttons on the Beoremote Halo to work with your Home automation to control all your Home Automation systems with an easily accessible and well crafted remote.
The API works with both the wall mounted and table versions of the Beoremote Halo.
Beoremote Halo supports adding buttons with icons or text for most general Home automation applications.
<img src="https://github.com/bang-olufsen/beoremote-halo/blob/main/Docs/Images/Halo%20flow%200.png" width=100% height=100% align="center">
<br />
### Connecting to Beoremote Halo
Connection to Beoremote Halo is done using a websocket client connecting to Beoremote Halos Websocket server using Beoremote Halos IP address on Port:8080.
Once connection is established a configuration must be sent to Beoremote Halo for it to configure the screens and buttons.
The Beoremote Halo will answer back if the configuration was successful or not.
<br />

<img src="https://github.com/bang-olufsen/beoremote-halo/blob/main/Docs/Images/HALO%20Flow1.png" width=100% height=100% align="center">


After configuration it is possible to set the status of each button, for example to show if something has changed in the setup.

<img src="https://github.com/bang-olufsen/beoremote-halo/blob/main/Docs/Images/HALO%20Flow2.png" width=70% height=70% align="center">


Halo will also send events on button press and wheel changes to the control system.

<img src="https://github.com/bang-olufsen/beoremote-halo/blob/main/Docs/Images/HALO%20Flow3.png" width=60% height=60% align="center">


For further details on the Open API including list of commands, examples and icons please also refer to the API description [here](https://bang-olufsen.github.io/beoremote-halo/)
