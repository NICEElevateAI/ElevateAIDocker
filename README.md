# ElevateAI Docker Image

This repo is for building the docker image of the Python SDK to upload a directory of files to ElevateAI.

## Docker Hub

To use the latest Docker Hub image instead of building your own image, copy config.json.sample to config.json, update the api_key in config.json and then run the following:

```sh
docker run --tty --rm --name elevateai \
  --volume $PWD/config.json:/usr/elevateai/config.json \
  --volume $PWD/input:/usr/elevateai/input elevateai/elevateai:latest
```

## Setup

Clone this repository and submodule:

```sh
git clone --recursive https://github.com/NICEElevateAI/ElevateAIDocker
cd ElevateAIDocker
```

### Create config.json

Copy config.json.sample to config.json and replace the api_key. If you don't have an API key, visit the [ElevateAI website](https://www.elevateai.com).

### Build

Build the image

```sh
docker build -t elevateai/elevateai:latest .
```

Place the audio files in a directory. Pass in the audio files directory and config.json.

Use the following to either run the build above or pull from Docker Hub:

```sh
docker run --tty --rm --name elevateai \
  --volume $PWD/config.json:/usr/elevateai/config.json \
  --volume $PWD/input:/usr/elevateai/input elevateai/elevateai:latest
```

