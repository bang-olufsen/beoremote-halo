# Beoremote Halo Home Automation Open API

<img src="https://github.com/bang-olufsen/beoremote-halo/blob/main/Docs/Images/Halo%20CI%20silver%20wall.png" width=40% height=40% align="right">



## Welcome
The Home Automation System API is an open source API that allows you to interact with a Beoremote Halo from a control system.
Using a websocket to communicate with the Beoremote Halo, it is possible to create a configuration of buttons on the Beoremote Halo to work with your Home automation to control all your Home Automation systems with an easily accessible and wellcrafted remote.
The API works with both the wall mounted and the table versions of the Beoremote Halo. 
<br />
<br />
You can find out more about Beoremote Halo on the Bang & Olufsen retail website [here](https://www.bang-olufsen.com/en/us/accessories/beoremote-halo): 
<br />
<br />
<br />

## Connecting to Beoremote Halo
Using the Beoremote Halo as an extension you can control your smart home devices that are connected to your Home Automation control system.
Beoremote Halo supports adding buttons with icons for most general Home automation applications and also has the option to create buttons with text. 
<img src="https://github.com/bang-olufsen/beoremote-halo/blob/main/Docs/Images/Halo%20flow%200.png" width=75% height=75% align="center">


Connection to Beoremote Halo is done using a websocket client connecting to Halos Websocket server using Beoremote Halos IP adress on Port:8080. 
Once connection is established a configuration must be sent to the remote for it to configure the screens and buttons. 
The Beoremote Halo will answer back with acknowledgements if the configuration was successful or not. 
<br />

<img src="https://github.com/bang-olufsen/beoremote-halo/blob/main/Docs/Images/HALO%20Flow1.png" width=85% height=85% align="center">


After configuration it is possible to set the status of each button, for example to show if something has changed in the setup. 

<img src="https://github.com/bang-olufsen/beoremote-halo/blob/main/Docs/Images/HALO%20Flow2.png" width=80% height=80% align="center">


Halo will also send events on button press and wheel changes to the control system. 

<img src="https://github.com/bang-olufsen/beoremote-halo/blob/main/Docs/Images/HALO%20Flow3.png" width=70% height=70% align="center">


For further details on the Open API including list of commands, examples and icons please also refer to the API description [here](https://bang-olufsen.github.io/beoremote-halo/)


## Python script
To get you started you can find a demo implementation created in Python in our examples folder [here](https://github.com/bang-olufsen/beoremote-halo/tree/main/examples)


#### Prerequisites
These examples have been tested using python3.9 and requires the following packages to run
```
pip3 install websocket-client zeroconf
```
#### Discover Beoremote Halo on the network
```
$ python3 discoverBeoremoteHalo.py
If Beoremote Halo does not appear on the list, try waking it up while discovering in running.
Press enter to exit...

BeoremoteHalo-xxxxxxxx.local
```

## Licence
License
Copyright 2021 Bang & Olufsen a/s

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
