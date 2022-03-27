# mycloud_recover

A recovery script for extracting data from a mycloud home device (https://www.westerndigital.com/products/cloud-storage/wd-my-cloud-home).

It requires the database and contents directory to be intact.

## Installation

```sh
# Not required, but recomended to install in a virtual env
python3 -m venv venv

pip install https://github.com/jthacker/mycloud_recover
```

## Usage

```sh
mycloud_recover /Volumes/BACKUP/backup/restsdk/ /Volumes/BACKUP/recovered
```
