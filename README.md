# [Accelerate SF] Backend

## Installation

### Setup Python Virtual Env

1. Create a venv named `.venv`

```bash
python3 -m venv .venv
```

2. Activate virtual environment (required every time when you need to start the app)

```bash
. .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## Start the Service

```bash
sh run.sh
```

### Setup AWS Credentials

1. Install AWS CLI if you haven't
   already. [Instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
2. Run `aws configure` and punch in the AWS credentials (ask @ShaneTsui)