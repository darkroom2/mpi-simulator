## Problem

_Check Erlang's formula. Propose a method to calculate what must be the maximum
traffic offered to a system in which we have N serving devices, and it is
required that the probability of loss does not exceed a given value._

## Solution

The proposed solution involves a simulator that generates with exponential
distribution the incoming packets to a system with N devices handling them.
After the simulation, the maximum traffic to the server is counted and
presented.

The simulator allows modifying the simulation parameters from the configuration
file.

## Analysis

DONE: Working Erlang B simulator.

TODO: Make Inverse Erlang B simulator.

---

## Requirements

`python >= 3.6`
`pip`
`numpy`

## Setup

### Install system requirements

* _Linux (Debian / Ubuntu):_

```commandline
sudo apt update
sudo apt install python3 python3-pip
```

* _Windows_

https://www.python.org/downloads/

This will install Python as well as `pip`

### Install Python requirements

```commandline
pip3 install numpy
```

---

### Usage

First, change the parameters in the [config.json](config/config.json)
file.

You can also create your own json file with all needed parameters, for example:

```json
{
  "lambda": 8,
  "mi": 8,
  "servers": 10,
  "simulation_time": 10
}
```

To run the simulator, use `main` script from `simulation` module:

```commandline
python3 -m simulator.main
```
