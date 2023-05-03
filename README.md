# Invoice Generator

## Purpose

Python script that generates invoice (only Czech language ATM)

## Prerequisites

### Dependencies

- [Docker](https://docs.docker.com/engine/install/)

### First step

- Clone this repo
- Enter it
- Copy [.env.example](./.env.example) to `.env`

```bash
git clone https://github.com/tomas223/invoice_generator
cd invoice_generator
cp .env.example .env
```

- Update env. variables.
  - Use symbol `|` _(pipe)_ as **line separator**.
  - Some variables are optional. For details check [settings.py](./settings.py) file

## How to run in Docker and convert to PDF automatically

**Build Docker container**

```bash
# Windows PowerShell, Linux & Mac
docker build -t invoices_python .

# Linux & Mac
make build
```

**Generate invoice report**

```bash
# Windows PowerShell, Linux & Mac
docker run -it --rm -v ${PWD}:/app invoices_python

# Linux & Mac
make invoice
```

- Now you can find your report in [output](./outpu) directory
