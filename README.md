# Quantified Self

## Introduction

Quantified Self is a habit tracking application. In this app you can track your habits on frequencies of your choice and can monitor performance of those.
It is built using flask and flask restful as backend framework and sqlite for database. VeuJs framework is used for frontend. Celery and Redis is used to perform background tasks.

## Installation

Clone the repository
``` bash
git clone git@github.com:ankushpotgante/QuantifiedSelf.git
cd QuantifiedSelf
```

Create a virtual environment

``` sh
python -m venv env
```

Activate the environment

For windows
```sh
env\Scripts\activate
```

For linux
``` sh
source env/bin/activate
```

Install dependencies

```sh
pip install -r requirements.txt
```

Give executalbe permission to scripts
``` bash
chmod +x celery-beat.sh run-celery.sh run-app.sh
```

## Configurations

Modify content in `application/config.py` as per your requirements


## Usage

Run Celery beat
``` bash
./celery-beat.sh
```

Run celery
``` bash
./run-celery.sh
```

Run the Application
``` bash
./run-app.sh
```

Open your browser and navigate to http://127.0.0.1:5000.