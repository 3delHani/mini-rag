# mini-rag-app

This is a minimal implementation of the rag model for question answering

## Requirements

python 3.14 or later 

### Install python using MiniConda

1) Download and install miniconda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2) Create new environment using the following command:

```bash
$ conda create -n mini-rag python = 14
```

3) Activate the environment: q

```bash
$ conda activate mini-rag
```

#### (Optional) setup your command line interface for better readability

```bash
export PS1="\[\033[01;32m\]u\@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install require packages

```bash
$ pip install -r requirements.txt
```

### Setup environment variables

```bash
$ cp .env.example .env
```

set your environment variables in the `.env` file like `OPENAI_API_KEY` value. 

## Run the FastAPI server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## Run Docker Compose Services

```bash
$ cd docker
$ sudo docker compose up -d
```

- update `.env` with your credentials
