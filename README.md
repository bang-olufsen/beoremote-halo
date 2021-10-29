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


### Python script
To get you started you can find a demo implementation created in Python in our examples folder [here](https://github.com/bang-olufsen/beoremote-halo/tree/main/examples)


#### Prerequisites
These examples have been tested using python 3.9 and requires the following packages to run
```commandline
$ pip3 install websocket-client zeroconf
```
#### Discover Beoremote Halo on the network
Discover Beoremote Halo on the network using mDNS service, a python script is provided for ease of use called discover.py:
```commandline
$ python discover.py
If Beoremote Halo does not appear on the list, try waking it up while discovery in running.
Press enter to exit...

BeoremoteHalo-XXXXXXXX.local
...
```
#### Home Automation Examples
Three examples are located in [examples](https://github.com/bang-olufsen/beoremote-halo/tree/main/examples).

## Licence
License
Copyright 2021 Bang & Olufsen a/s

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
