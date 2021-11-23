## Problem

_Check Erlang's formula. Propose a method to calculate what must be the maximum
traffic offered to a system in which we have N serving devices, and it is
required that the probability of loss does not exceed a given value._

## Solution

A naive method of checking Erlang's formula for a given number of serving
devices and a given packet blocking probability involves calculating the maximum
traffic offered to the server (using a formula and a numerical method) and
running a simulation in which the previously calculated traffic is a parameter
and checking whether the simulation-calculated probability is close to the given
one.

The simulator allows modifying the simulation parameters in
the [config/config.json](config/config.json) file.

## TODO

* Making simulation independent of formula-calculated max traffic value.

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

First, change the parameters in its configuration file.

You can also create your own json file with all needed parameters, for example:

```json
{
  "lambda": 1,
  "servers": 5,
  "simulation_time": 5,
  "blocking_probability": 0.2,
  "seed": 123,
  "show_plots": true
}
```

To run the simulator, use `main` script from `simulation` module:

```commandline
python3 -m simulator.main
```
