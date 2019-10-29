# Energy Measurement and Cloud Storage With a FiPy Board
#### *Moises Daniel Garcia Rojas*
#### *October 29, 2019*

## Project Overview

The FiPy board is interfaced with a PZEM-004T-100A(V3.0) sensor. The interaction of the two monitors energy variables, which then are uploaded to the Pybytes platform to store and visualize the data.


### Folder Structure
```
.
├── lib
│   ├── CRC16.py
│   └── PZEM_100A_V3.py
├── boot.py
├── main.py
└── README.md
```

### Files description

* CRC16.py: A module to perform Cyclic Redundancy Test of 16 bits on the data received from the PZEM-004T-100A(V3.0) sensor (the generator polynomial and the seed value can be modified to match other applications)
* PZEM_100A_v3.py: Module whith methods to interact with the PZEM-004T-100A(V3.0) sensor through RS-232 (This module is intended to provide simple communication functionalities between the FiPy board and the PZEM sensor, and are enough for the current project. If more complex interactions are required the user must modifiy the code)
* boot.py: Empty file which is required by the device to work properly (it should contain a script to boot the device in case de boot-GPIO is in use)
* main.py: main script that interacts with the PZEM-004T-100A(V3.0) sensor
* README.md: General explanation of the project

## NOTE

In order for the device to be connected to the wifi and to communicate with the server, the device must be flashed with the pybytes firmware using the correct modem-router credentials. The other option is to flash the proper libraries.

For further information refer to the <a href="https://docs.pycom.io/">Pycom documentation</a>
