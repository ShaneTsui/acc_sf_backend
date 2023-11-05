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

### Set up PostgreSQL

1. Install PostgresSQL with brew

```
brew install postgresql
```

2. Enter postgres terminal (use either command)

```shell
$ psql -d postgres -U $(whoami)

# If command above does not work, then try this one
$ sudo -u postgres psql
```

3. Create user (replace `<username>` and `<password>` with your own values)

```postgresql
CREATE USER <username>;
alter
user
<username>
with encrypted password '<password>';

-- Optional: grant superuser permission --
ALTER
USER
<username>
WITH SUPERUSER;
```

4. Create database and grant permission (replace `<username>` with your own value)

```
CREATE DATABASE acc_sf;

grant all privileges on database acc_sf to <username>;
```

5. Set up the following env variables (replace `<password>` with your own value)

```
export POSTGRES_USERNAME="$(whoami)"
export POSTGRES_PASSWORD="<password>"
export DATABASE_URL="postgresql://$POSTGRES_USERNAME:$POSTGRES_PASSWORD@localhost:5432"
```

## Start the Service

```bash
sh run.sh
```

### Setup AWS Credentials

1. Install AWS CLI if you haven't
   already. [Instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
2. Run `aws configure` and punch in the AWS credentials (ask @ShaneTsui)