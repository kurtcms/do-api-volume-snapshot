# DigitalOcean API: Create and Rotate Volume Snapshot

This Python app is containerised with [Docker Compose](https://docs.docker.com/compose/) for a modular and cloud native deployment that fits in any microservice architecture.

It does the following:

1. Call the [DigitalOcean (DO) API](#reference) to create a snapshot from a volume; and
2. Rotate the volume snapshot by removing the obsolete one(s). 

A detailed walk-through is available [here](https://kurtcms.org/digitalocean-api-create-and-rotate-volume-snapshot/).

## Table of Content

- [Getting Started](#getting-started)
  - [Git Clone](#git-clone)
  - [Environment Variable](#environment-variables)
  - [Crontab](#crontab)
  - [Docker Container](#docker-container)
	  - [Docker Compose](#docker-compose)
	  - [Build and Run](#build-and-run)
  - [Standalone Python Script](#standalone-python-script)
    - [Dependencies](#dependencies)
    - [Cron](#cron)
- [Docker Logs](#docker-logs)
- [Reference](#reference)

## Getting Started

Get started in three simple steps:

1. [Download](#git-clone) a copy of the app;
2. Create the [environment variables](#environment-variables) for the DO authentication and modify the [crontab](#crontab) if needed; and
3. [Docker Compose](#docker-compose) or [build and run](#build-and-run) the image manually to start the app, or alternatively run the Python script as a standalone service.

### Git Clone

Download a copy of the app with `git clone`
```shell
$ git clone https://github.com/kurtcms/do-api-volume-snapshot /app/
```

### Environment Variables

The app expects the base URL, the API token, the DO volume ID and the number of volume snapshot to keep, as environment variables in a `.env` file in the same directory.

Be sure to create the `.env` file.

```shell
$ nano /app/do-api-volume-snapshot/.env
```

And define the variables accordingly.

```
DO_BASE_URL = 'https://api.digitalocean.com/v2'
DO_TOKEN = '(redacted)'

# ID of the volume
DO_VOLUME_ID = '(redacted)'

# Number of volume snapshot to keep
DO_SNAPSHOT = 1
```

### Crontab

By default the app is scheduled with [cron](https://linux.die.net/man/8/cron) to create and rotate the volume snapshot everyday, with `stdout` and `stderr` redirected to the main process for `Docker logs`.  

Modify the `crontab` if a different schedule is required.

```shell
$ nano /app/do-api-volume-snapshot/crontab
```

### Docker Container

Packaged as a container, the app is a standalone, executable package that may be run on Docker Engine. Be sure to have [Docker](https://docs.docker.com/engine/install/) installed.

#### Docker Compose

With Docker Compose, the app may be provisioned with a single command. Be sure to have [Docker Compose](https://docs.docker.com/compose/install/) installed.

```shell
$ docker-compose up -d
```

Stopping the container is as simple as a single command.

```shell
$ docker-compose down
```

#### Build and Run

Otherwise the Docker image can also be built manually.

```shell
$ docker build -t do_api_volume_snapshot /app/do-api-volume-snapshot/
```

Run the image with Docker once it is ready.  

```shell
$ docker run -it --rm --name do_api_volume_snapshot do_api_volume_snapshot
```

### Standalone Python Script

Alternatively the `do_api_volume_snapshot.py` script may be deployed as a standalone service.

#### Dependencies

In which case be sure to install the following required libraries for the `do_api_volume_snapshot.py`:

1. [Requests](https://github.com/psf/requests)
2. [Python-dotenv](https://github.com/theskumar/python-dotenv)

```shell
$ pip3 install requests python-dotenv
```

#### Cron

The script may then be executed with a task scheduler such as [cron](https://linux.die.net/man/8/cron) that runs it everyday for example.

```shell
$ (crontab -l; echo "0 0 * * * /usr/bin/python3 /app/do-api-volume-snapshot/do_api_volume_snapshot.py") | crontab -
```

## Docker Logs

A message will be printed on the creation and the deletion of volume snapshot. 

```
Snapshot 2022-10-21-00-00-02 is created at 2022-10-21T00:00:02Z
Snapshot 2022-10-20-00-00-02 is removed at 2022-10-21T00:00:06Z
```

## Reference

- [DigitalOcean API (2.0)](https://docs.digitalocean.com/reference/api/api-reference/)
