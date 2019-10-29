# pcpartpicker

[![Build Status](https://travis-ci.org/JonathanVusich/pcpartpicker.svg?branch=master)](https://travis-ci.org/JonathanVusich/pcpartpicker)
[![Coverage Status](https://coveralls.io/repos/github/JonathanVusich/pcpartpicker/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/JonathanVusich/pcpartpicker?branch=master&kill_cache=1)
![](https://img.shields.io/pypi/dm/pcpartpicker.svg)

This is an unofficial Python 3.7+ API for the website pcpartpicker.com.
It is written using asynchronous requests for efficient data retrieval. 
This package is currently in a stable beta.

## Installation:
Package retrieval and installation can be easily accomplished through pip.
```python
pip install pcpartpicker
```

## Examples:
In order to use the API, simply import API from the pcpartpicker package.
```python
from pcpartpicker import API
```
You can then instantiate the API class and use it to make requests.
```python
api = API()
cpu_data = api.retrieve("cpu")
all_data = api.retrieve_all()
```
`api.retrieve()` and `api.retrieve_all()` methods both return a `PartData` instance, which contains a timestamp and a `to_json()` method. 

A list of supported parts can be obtained in the following manner:
```python
api = API()
print(api.supported_parts)
>>> {'wireless-network-card', 'case-fan', 'cpu', 'cpu-cooler', 'headphones', 'motherboard', 'monitor', 'internal-hard-drive', 'external-hard-drive', 'ups', 'fan-controller', 'case', 'keyboard', 'mouse', 'wired-network-card', 'sound-card', 'video-card', 'speakers', 'optical-drive', 'power-supply', 'thermal-paste', 'memory'}
```

There are also a number of methods that can be used in order to customize the API behavior.
For example, you can change the region, determine the number of concurrent, asynchronous connections
that can be made, and can also set whether or not the API can use multiple threads.

Retrieving supported API regions:
```python
api = API()
print(api.supported_regions)
>>> {'be', 'us', 'it', 'uk', 'ie', 'nz', 'de', 'ca', 'au', 'fr', 'se', 'es', 'in'}
```

Retrieving currently selected region (default is US):
```python
api = API()
print(api.region)
>>> us
```

Creating an API object with a different default region:
```python
api = API("de")
print(api.region)
>>> de
```

Changing the default region:
```python
api = API()
api.set_region("de")
print(api.region)
>>> de
```
