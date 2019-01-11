# pcpartpicker

[![Build Status](https://travis-ci.org/JonathanVusich/pcpartpicker.svg?branch=master)](https://travis-ci.org/JonathanVusich/pcpartpicker)
[![Coverage Status](https://coveralls.io/repos/github/JonathanVusich/pcpartpicker/badge.svg)](https://coveralls.io/github/JonathanVusich/pcpartpicker)
![](https://img.shields.io/pypi/dm/pcpartpicker.svg)

This is an unofficial Python 3.7+ API for the website pcpartpicker.com.
Written using async code and multiprocessing for efficient data retrieval. 
This package is currently in beta.

## Installation:
```
pip install pcpartpicker
```

## Examples:
Retrieving supported API regions:
```
from pcpartpicker import API

api = API()
print(api.supported_regions)
>>> {'be', 'us', 'it', 'uk', 'ie', 'nz', 'de', 'ca', 'au', 'fr', 'se', 'es', 'in'}
```

Retrieving currently selected region (default is US):
```
from pcpartpicker import API

api = API()
print(api.region)
>>> us
```

Creating an API object with a different default region:
```
from pcpartpicker import API

api = API("de")
print(api.region)
>>> de
```

Changing the default region:
```
from pcpartpicker import API

api = API()
api.set_region("de")
print(api.region)
>>> de
```

Retrieving supported part list:
```
from pcpartpicker import API

api = API()
print(api.supported_parts)
>>> {'wireless-network-card', 'case-fan', 'cpu', 'cpu-cooler', 'headphones', 'motherboard', 'monitor', 'internal-hard-drive', 'external-hard-drive', 'ups', 'fan-controller', 'case', 'keyboard', 'mouse', 'wired-network-card', 'sound-card', 'video-card', 'speakers', 'optical-drive', 'power-supply', 'thermal-paste', 'memory'}
```

Retrieving all part data:
```
from pcpartpicker import API

api = API()
part_data = api.retrieve_all()
``` 

Retrieving specific part data:
```
from pcpartpicker import API

api = API()
cpu_data = api.retrieve("cpu")
```
