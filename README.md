# pcpartpicker

[![Build Status](https://travis-ci.org/JonathanVusich/pcpartpicker.svg?branch=master)](https://travis-ci.org/JonathanVusich/pcpartpicker)
[![Coverage Status](https://coveralls.io/repos/github/JonathanVusich/pcpartpicker/badge.svg)](https://coveralls.io/github/JonathanVusich/pcpartpicker)

This is an unofficial Python 3.7+ API for the website pcpartpicker.com.
Written using async code and multiprocessing for efficient data retrieval. 
This package is currently in beta.

## Installation:
```buildoutcfg
pip install pcpartpicker
```

## Examples:

Retrieving all part data:
```buildoutcfg
from pcpartpicker import API

api = API()
part_data = api.retrieve_all()
``` 

Retrieving specific part data:
```buildoutcfg
from pcpartpicker import API

api = API()
cpu_data = api.retrieve("cpu")
```

Changing the region:
```buildoutcfg
from pcpartpicker import API

api = API("se")
```

Alternative method of changing the region:
```buildoutcfg
from pcpartpicker import API

api = API()
api.set_region("in")
```
