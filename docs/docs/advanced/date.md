


## Overview

**Arrow** is used as the date library in Assembly,  and `date` is the alias available. Arrow helps you work with dates and times with fewer imports and a lot less code.

Extension: <a href="https://arrow.readthedocs.io/en/latest/" target="_blank">Arrow</a>

---

## Usage

### Import

```python
from assembly import date
```

### Usage

```python
from assembly import date

date.get('2013-05-11T21:23:58.970460+07:00')
#-> <Arrow [2013-05-11T21:23:58.970460+07:00]>

utc = date.utcnow()
#-> <Arrow [2013-05-11T21:23:58.970460+00:00]>

utc = utc.shift(hours=-1)
#-> <Arrow [2013-05-11T20:23:58.970460+00:00]>

local = utc.to('US/Pacific')
#-> <Arrow [2013-05-11T13:23:58.970460-07:00]>

local.timestamp
#-> 1368303838

local.format()
#-> '2013-05-11 13:23:58 -07:00'

local.format('YYYY-MM-DD HH:mm:ss ZZ')
#-> '2013-05-11 13:23:58 -07:00'

local.humanize()
# 'an hour ago'

```

or along with config

```python
from assembly import date, config

local = utc.to(config.get('TIMEZONE'))

local.format(config.get('DATE_FORMAT.default'))

```

---

## Supported Tokens


Use the following tokens in parsing and formatting. Note that they’re not the same as the tokens for strptime. <a href="https://arrow.readthedocs.io/en/latest/#supported-tokens" target="_blank">View all supported tokens</a>


```
ie:
local = utc.to('US/Pacific')
local.format('YYYY-MM-DD HH:mm:ss')

**Year**
-- YYYY (2019, 2020)
-- YY (19, 20)

**Month**
-- MMMM (January, February,...)
-- MMM (Jan, Feb, ...)
-- MM (01, 02, ...)
-- M (1, 2, ...)

**Dat of Year**
-- DDDD (001, 002, ..., 364, 365)
--- DDD (01, 02, 364, 365)

**Day of Month**
-- DD (01, 02, ..., 30, 31)
-- D (1, 2,..., 30, 31)
-- Do (1st, 2nd, ..., 30th, 31st)

**Day of Week**
-- dddd (Monday, Tuesday)
-- dd (Mon, Tues)
-- d (1,2, ..., 6,7)

**Hour**
-- HH (00, 01, ... 23)
-- H (1, 23)
-- hh (01, 02, ..., 11, 12)
-- h (1, 2, ..., 11, 12)

**AM/PM**
-- A (AM, PM)
-- a (am, pm)

**Minute**
-- mm (00, 01, ..., 59)
-- m (0, 1, ..., 59)

**Second**
-- ss (00, 01, ..., 59)
-- s (0, 1, ..., 59)

```

---


