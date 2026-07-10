# Matrimony Platform — Master Local Development Setup

> **Version:** 1.1  
> **Last updated:** 10 July 2026  
> **Environment:** Windows 11 + WSL2 + Ubuntu 22.04  
> **Purpose:** This is the master guide for installing and configuring the complete local development environment for the Matrimony platform on a new Windows machine.

---

## 1. Technology Stack

| Component | Technology / Version |
|---|---|
| Host operating system | Windows 11 |
| Linux environment | WSL2 |
| Linux distribution | Ubuntu 22.04 LTS |
| Web server | Nginx |
| Frontend language | PHP 8.3 |
| Frontend framework | CodeIgniter 4 |
| Dependency manager | Composer |
| Backend language | Python 3.12 |
| Backend framework | FastAPI |
| ORM | SQLAlchemy |
| Database migrations | Alembic |
| Database | PostgreSQL 16 |
| Cache | Redis |
| Source control | Git |
| IDE | VS Code + Remote WSL |
| Git hosting | GitHub using SSH authentication |

---

## 2. Local Domains

The local environment uses separate domains for the frontend and backend.

| Domain | Purpose | Served by |
|---|---|---|
| `http://sikhanandkaraj.local` | CodeIgniter frontend | Nginx + PHP-FPM |
| `http://api.sikhanandkaraj.local` | FastAPI backend | Nginx reverse proxy to FastAPI |

The FastAPI application will normally listen internally on:

```text
http://127.0.0.1:8000
```

Port `8000` is not accessed directly by the browser after Nginx is configured.

---

## 3. Project Paths

### Windows path

```text
D:\www\webapp-matrimony
```

### WSL path

```text
/mnt/d/www/webapp-matrimony
```

### Recommended project structure

```text
D:\www\webapp-matrimony
├── frontend
├── backend
├── database
├── deployment
├── docs
├── scripts
├── .gitignore
└── README.md
```

Create the directories from WSL if they do not already exist:

```bash
mkdir -p /mnt/d/www/webapp-matrimony/{frontend,backend,database,deployment,docs,scripts}
```

---

## 4. Install WSL2 and Ubuntu 22.04

Open **PowerShell as Administrator** and run:

```powershell
wsl --install Ubuntu-22.04
```

Restart Windows if requested.

### Verify WSL

```powershell
wsl --list --verbose
```

Expected result:

```text
NAME             STATE     VERSION
Ubuntu-22.04     Running   2
```

If Ubuntu is not using WSL2:

```powershell
wsl --set-version Ubuntu-22.04 2
```

Optionally make it the default distribution:

```powershell
wsl --set-default Ubuntu-22.04
```

---

## 5. Update Ubuntu

Open Ubuntu and run:

```bash
sudo apt update
sudo apt upgrade -y
```

### Verify Ubuntu version

```bash
lsb_release -a
```

Expected:

```text
Ubuntu 22.04 LTS
```

---

## 6. Install Base Utilities

```bash
sudo apt install -y \
    curl \
    gnupg \
    lsb-release \
    unzip \
    vim \
    software-properties-common
```

---

## 7. Install Git

```bash
sudo apt install git -y
```

### Verify Git

```bash
git --version
```

Configure your Git identity:

```bash
git config --global user.name "Anant Singh"
git config --global user.email "info@sikhanandkaraj.com"
```

Verify:

```bash
git config --global --list
```

---

## 8. Install VS Code Remote WSL

Install the following on Windows:

1. Visual Studio Code
2. The **WSL** extension published by Microsoft

Navigate to the project from Ubuntu:

```bash
cd /mnt/d/www/webapp-matrimony
code .
```

### Checkpoint

The bottom-left corner of VS Code should show that the workspace is connected to WSL Ubuntu.

---

## 9. Install Nginx

```bash
sudo apt install nginx -y
```

Enable and start Nginx:

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
```

### Verify Nginx

```bash
nginx -v
sudo systemctl status nginx --no-pager
```

Expected status:

```text
active (running)
```

---

## 10. Install PHP 8.3

Install PHP 8.3 and the extensions required by CodeIgniter and PostgreSQL:

```bash
sudo apt install \
    php8.3 \
    php8.3-cli \
    php8.3-fpm \
    php8.3-common \
    php8.3-pgsql \
    php8.3-mbstring \
    php8.3-intl \
    php8.3-curl \
    php8.3-xml \
    php8.3-zip \
    php8.3-gd \
    php8.3-bcmath \
    php8.3-opcache \
    -y
```

Enable and start PHP-FPM:

```bash
sudo systemctl enable php8.3-fpm
sudo systemctl start php8.3-fpm
```

### Verify PHP

```bash
php -v
php -m
sudo systemctl status php8.3-fpm --no-pager
```

Expected:

```text
PHP 8.3.x
```

Verify the PHP-FPM socket:

```bash
ls -l /run/php/php8.3-fpm.sock
```

---

## 11. Install Composer

```bash
sudo apt install composer -y
```

### Verify Composer

```bash
composer --version
```

Expected:

```text
Composer version 2.x
```

---

## 12. CodeIgniter Frontend Location

The CodeIgniter application must be installed inside:

```text
/mnt/d/www/webapp-matrimony/frontend
```

Its public entry point must be:

```text
/mnt/d/www/webapp-matrimony/frontend/public/index.php
```

Nginx must expose only the `frontend/public` directory, never the CodeIgniter project root.

### Directory checkpoint

```bash
test -f /mnt/d/www/webapp-matrimony/frontend/public/index.php \
    && echo "CodeIgniter public/index.php found" \
    || echo "CodeIgniter has not yet been installed"
```

No `php spark serve` command is used in this project.

---

## 13. Install PostgreSQL 16

Import the PostgreSQL repository signing key:

```bash
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \
    | sudo gpg --dearmor \
    -o /usr/share/keyrings/postgresql.gpg
```

Add the PostgreSQL repository:

```bash
echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt jammy-pgdg main" \
    | sudo tee /etc/apt/sources.list.d/pgdg.list
```

Update package information:

```bash
sudo apt update
```

Install PostgreSQL 16:

```bash
sudo apt install \
    postgresql-16 \
    postgresql-client-16 \
    postgresql-contrib \
    -y
```

Enable and start PostgreSQL:

```bash
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

### Verify PostgreSQL

```bash
psql --version
sudo systemctl status postgresql --no-pager
```

Expected:

```text
psql (PostgreSQL) 16.x
```

---

## 14. Create the Development Database

Open PostgreSQL:

```bash
sudo -u postgres psql
```

For a new installation, create the database user first and make it the database owner:

```sql
CREATE USER matrimony_dev_user
WITH PASSWORD 'REPLACE_WITH_A_STRONG_LOCAL_PASSWORD';

CREATE DATABASE matrimony_dev
WITH OWNER = matrimony_dev_user
ENCODING = 'UTF8';

\c matrimony_dev

GRANT ALL ON SCHEMA public TO matrimony_dev_user;

\q
```

Do not use the sample password in a shared or production environment.

### Existing database correction

If the database was already created using the earlier commands, set the application user as its owner:

```bash
sudo -u postgres psql
```

```sql
ALTER DATABASE matrimony_dev OWNER TO matrimony_dev_user;

\c matrimony_dev

ALTER SCHEMA public OWNER TO matrimony_dev_user;
GRANT ALL ON SCHEMA public TO matrimony_dev_user;

\q
```

### Verify database login

```bash
psql \
    -h 127.0.0.1 \
    -U matrimony_dev_user \
    -d matrimony_dev \
    -c "SELECT current_database(), current_user;"
```

Enter the development password when prompted.

Expected values:

```text
current_database: matrimony_dev
current_user: matrimony_dev_user
```

---

## 15. Install Redis

```bash
sudo apt install redis-server -y
```

Enable and start Redis:

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

### Verify Redis

```bash
redis-cli ping
```

Expected:

```text
PONG
```

Check the service:

```bash
sudo systemctl status redis-server --no-pager
```

For local development, Redis should remain bound to localhost and must not be publicly exposed.

Verify:

```bash
sudo grep -E '^(bind|protected-mode)' /etc/redis/redis.conf
```

---

## 16. Install Python 3.12

Verify whether Python 3.12 is already installed:

```bash
python3.12 --version
```

If it is not available, install it:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    -y
```

### Verify Python

```bash
python3.12 --version
which python3.12
```

Expected:

```text
Python 3.12.x
```

---

## 17. Create the FastAPI Virtual Environment

The virtual environment is stored in the WSL Linux filesystem for better package-installation performance:

```text
/home/<linux-user>/venvs/webapp-matrimony
```

The source code remains on the Windows drive.

Navigate to the backend:

```bash
cd /mnt/d/www/webapp-matrimony/backend
```

Create the virtual environment:

```bash
mkdir -p ~/venvs
python3.12 -m venv ~/venvs/webapp-matrimony
```

Activate it:

```bash
source ~/venvs/webapp-matrimony/bin/activate
```

### Verify the active interpreter

```bash
python --version
which python
```

Expected:

```text
Python 3.12.x
/home/<linux-user>/venvs/webapp-matrimony/bin/python
```

---

## 18. Upgrade Python Packaging Tools

With the virtual environment active:

```bash
python -m pip install --upgrade pip setuptools wheel
```

Verify:

```bash
pip --version
```

---

## 19. Install FastAPI Dependencies

With the virtual environment active and while inside the backend directory:

```bash
pip install \
    fastapi \
    "uvicorn[standard]" \
    sqlalchemy \
    alembic \
    redis \
    psycopg2-binary \
    "python-jose[cryptography]" \
    "passlib[bcrypt]" \
    bcrypt \
    pydantic-settings \
    python-multipart \
    httpx \
    email-validator \
    orjson \
    python-dotenv \
    loguru \
    slowapi \
    itsdangerous \
    aiofiles \
    jinja2
```

Create the dependency lock list:

```bash
pip freeze > requirements.txt
```

### Verify major packages

```bash
pip show fastapi uvicorn sqlalchemy alembic redis psycopg2-binary
```

Confirm that `requirements.txt` exists:

```bash
ls -lh /mnt/d/www/webapp-matrimony/backend/requirements.txt
```

---

## 20. Create the Virtual Environment Alias

Add an alias that opens the backend directory and activates the virtual environment:

```bash
echo "alias matrimony-api='cd /mnt/d/www/webapp-matrimony/backend && source ~/venvs/webapp-matrimony/bin/activate'" \
    >> ~/.bashrc
```

Reload Bash:

```bash
source ~/.bashrc
```

Use the alias:

```bash
matrimony-api
```

### Verify

```bash
pwd
which python
```

Expected:

```text
/mnt/d/www/webapp-matrimony/backend
/home/<linux-user>/venvs/webapp-matrimony/bin/python
```

---

## 21. Configure Windows Local Domain Resolution

Open the following file as Administrator in Notepad:

```text
C:\Windows\System32\drivers\etc\hosts
```

Add:

```text
127.0.0.1 sikhanandkaraj.local
127.0.0.1 api.sikhanandkaraj.local
```

Save the file.

Flush the Windows DNS cache from an Administrator PowerShell:

```powershell
ipconfig /flushdns
```

### Verify from Windows

```powershell
ping sikhanandkaraj.local
ping api.sikhanandkaraj.local
```

Both domains should resolve to:

```text
127.0.0.1
```

The ping response itself may be blocked; name resolution to `127.0.0.1` is the important checkpoint.

---

## 22. Create the Nginx Configuration

The Nginx configuration file must be created at:

```text
/etc/nginx/sites-available/matrimony.conf
```

Create or edit it:

```bash
sudo vim /etc/nginx/sites-available/matrimony.conf
```

Use the following configuration:

```nginx
# CodeIgniter frontend over HTTP.
server {
    listen 80;

    server_name sikhanandkaraj.local;

    root /mnt/d/www/webapp-matrimony/frontend/public;
    index index.php index.html;

    access_log /var/log/nginx/matrimony_frontend_access.log;
    error_log  /var/log/nginx/matrimony_frontend_error.log;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    # Execute only real PHP files.
    location ~ \.php$ {
        try_files $uri =404;

        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.3-fpm.sock;        
    }

    # Block hidden files such as .env and .git.
    location ~ /\.(?!well-known).* {
        deny all;
    }

    # Prevent execution of PHP files from uploaded/static directories.
    location ~* ^/(uploads|assets)/.*\.php$ {
        deny all;
    }
}

server {
    listen 80;
    listen [::]:80;

    server_name api.sikhanandkaraj.local;

    access_log /var/log/nginx/sikhanandkaraj_api_access.log;
    error_log /var/log/nginx/sikhanandkaraj_api_error.log;

    location / {
        proxy_pass http://127.0.0.1:8000;

        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 10s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### Notes

- The frontend document root is the CodeIgniter `public` directory.
- FastAPI listens only on `127.0.0.1:8000`.
- The same local certificate covers both domains.
- API port `8000` does not need to be exposed publicly.

---

## 23. Enable the Nginx Site

Remove the default site to avoid conflicts:

```bash
sudo rm -f /etc/nginx/sites-enabled/default
```

Create the symbolic link:

```bash
sudo ln -s \
    /etc/nginx/sites-available/matrimony.conf \
    /etc/nginx/sites-enabled/matrimony.conf
```

If the link already exists, this is not an error. Verify it:

```bash
ls -l /etc/nginx/sites-enabled/
```

Test the configuration:

```bash
sudo nginx -t
```

Expected:

```text
syntax is ok
test is successful
```

Restart Nginx:

```bash
sudo systemctl restart nginx
```

Verify:

```bash
sudo systemctl status nginx --no-pager
```

---

## 24. Configure the CodeIgniter Local Environment

Create the CodeIgniter environment file from its template if it does not exist:

```bash
cd /mnt/d/www/webapp-matrimony/frontend
cp env .env
```

Edit:

```bash
vim .env
```

Add or update:

```dotenv
CI_ENVIRONMENT = development

app.baseURL = 'http://sikhanandkaraj.local/'

API_BASE_URL = 'http://api.sikhanandkaraj.local'
```

Do not commit the real `.env` file.

Ensure the CodeIgniter writable directory is available:

```bash
mkdir -p writable/{cache,logs,session,uploads}
```

For local development on the mounted Windows drive, confirm Nginx/PHP can write to it. Begin with:

```bash
chmod -R ug+rwX writable
```

If PHP-FPM receives permission errors, inspect:

```bash
sudo tail -n 100 /var/log/nginx/matrimony_frontend_error.log
```

Avoid using `chmod -R 777`.

---

## 25. Configure the FastAPI Local Environment

Create:

```text
/mnt/d/www/webapp-matrimony/backend/.env
```

Example:

```dotenv
APP_ENV=development
APP_NAME=Matrimony API
APP_URL=http://api.sikhanandkaraj.local

DATABASE_URL=postgresql+psycopg2://matrimony_dev_user:REPLACE_WITH_URL_ENCODED_PASSWORD@127.0.0.1:5432/matrimony_dev

REDIS_URL=redis://127.0.0.1:6379/0

CORS_ORIGINS=["http://sikhanandkaraj.local"]

JWT_SECRET=REPLACE_WITH_A_LONG_RANDOM_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Generate a strong local JWT secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Do not commit `.env`.

---

## 26. Start the FastAPI Backend

Activate the environment:

```bash
matrimony-api
```

Assuming the FastAPI application object is `app` inside `app/main.py`, run:

```bash
uvicorn main:app \
    --host 127.0.0.1 \
    --port 8000 \
    --reload
```

Do not bind the local development API to `0.0.0.0` unless access from another machine is intentionally required.

### Verify the internal API

Open another WSL terminal:

```bash
curl -I http://127.0.0.1:8000/docs
```

---


## 27. Daily Startup Procedure

Open Ubuntu or the project in VS Code Remote WSL.

Navigate to and activate the backend:

```bash
matrimony-api
```

Check services:

```bash
sudo systemctl status nginx --no-pager
sudo systemctl status php8.3-fpm --no-pager
sudo systemctl status postgresql --no-pager
sudo systemctl status redis-server --no-pager
```

Start any stopped service:

```bash
sudo systemctl start nginx
sudo systemctl start php8.3-fpm
sudo systemctl start postgresql
sudo systemctl start redis-server
```

Start FastAPI:

```bash
uvicorn main:app \
    --host 127.0.0.1 \
    --port 8000 \
    --reload
```

Open:

```text
http://sikhanandkaraj.local
http://api.sikhanandkaraj.local/docs
```

---

## 28. Complete Environment Verification

Run:

```bash
echo "=== Ubuntu ==="
lsb_release -ds

echo "=== Nginx ==="
nginx -v

echo "=== PHP ==="
php -v | head -n 1

echo "=== Composer ==="
composer --version

echo "=== PostgreSQL ==="
psql --version

echo "=== Redis ==="
redis-cli ping

echo "=== Python ==="
python3.12 --version

echo "=== Git ==="
git --version

echo "=== Nginx configuration ==="
sudo nginx -t
```

With the virtual environment active:

```bash
echo "=== Active Python ==="
which python

echo "=== FastAPI ==="
python -c "import fastapi; print(fastapi.__version__)"

echo "=== SQLAlchemy ==="
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

---

## 29. Installation Checklist

- [ ] WSL2 installed
- [ ] Ubuntu 22.04 installed
- [ ] Project directories created on the Windows drive
- [ ] VS Code Remote WSL working
- [ ] Git installed
- [ ] GitHub SSH authentication working
- [ ] Nginx installed and running
- [ ] PHP 8.3 installed
- [ ] PHP-FPM running
- [ ] Composer installed
- [ ] CodeIgniter frontend present under `frontend`
- [ ] PostgreSQL 16 installed and running
- [ ] `matrimony_dev` database created
- [ ] `matrimony_dev_user` created
- [ ] Database login verified
- [ ] Redis installed and responding with `PONG`
- [ ] Python 3.12 installed
- [ ] Python virtual environment created
- [ ] FastAPI dependencies installed
- [ ] `requirements.txt` generated
- [ ] `matrimony-api` alias working
- [ ] Windows hosts file contains both local domains
- [ ] Nginx configuration created in `sites-available`
- [ ] Nginx symbolic link created in `sites-enabled`
- [ ] Nginx configuration test passes
- [ ] `http://sikhanandkaraj.local` opens without a certificate warning
- [ ] `http://api.sikhanandkaraj.local/docs` opens without a certificate warning

---

## 30. Common Troubleshooting

### Nginx configuration test fails

```bash
sudo nginx -t
```

Inspect the exact file and line number shown in the error.

View logs:

```bash
sudo tail -n 100 /var/log/nginx/error.log
sudo tail -n 100 /var/log/nginx/matrimony_frontend_error.log
sudo tail -n 100 /var/log/nginx/matrimony_api_error.log
```

---

### Domain does not resolve

Check the Windows hosts file:

```text
C:\Windows\System32\drivers\etc\hosts
```

Required entries:

```text
127.0.0.1 sikhanandkaraj.local
127.0.0.1 api.sikhanandkaraj.local
```

Flush DNS:

```powershell
ipconfig /flushdns
```

---

### Frontend returns 404 or exposes the wrong directory

Confirm the Nginx root is:

```text
/mnt/d/www/webapp-matrimony/frontend/public
```

It must not be:

```text
/mnt/d/www/webapp-matrimony/frontend
```

Verify:

```bash
ls -l /mnt/d/www/webapp-matrimony/frontend/public/index.php
```

---

### PHP file downloads instead of executing

Check PHP-FPM:

```bash
sudo systemctl status php8.3-fpm --no-pager
```

Verify the socket:

```bash
ls -l /run/php/php8.3-fpm.sock
```

Then test and restart:

```bash
sudo nginx -t
sudo systemctl restart php8.3-fpm
sudo systemctl restart nginx
```

---

### API returns 502 Bad Gateway

FastAPI is probably not running on port `8000`.

Check:

```bash
ss -ltnp | grep 8000
```

Start it:

```bash
matrimony-api
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Inspect the API Nginx log:

```bash
sudo tail -n 100 /var/log/nginx/matrimony_api_error.log
```

---

### PostgreSQL authentication fails

Test explicitly:

```bash
psql \
    -h 127.0.0.1 \
    -U matrimony_dev_user \
    -d matrimony_dev
```

Check PostgreSQL status:

```bash
sudo systemctl status postgresql --no-pager
```

---

### Redis is unavailable

```bash
sudo systemctl restart redis-server
redis-cli ping
```

Expected:

```text
PONG
```

---

### Virtual environment is not active

```bash
source ~/venvs/webapp-matrimony/bin/activate
```

Or:

```bash
matrimony-api
```

Verify:

```bash
which python
```

---

### Services do not start automatically in WSL

Check whether systemd is enabled:

```bash
ps -p 1 -o comm=
```

Expected:

```text
systemd
```

If systemd is not active, create or edit:

```bash
sudo vim /etc/wsl.conf
```

Add:

```ini
[boot]
systemd=true
```

From Windows PowerShell:

```powershell
wsl --shutdown
```

Reopen Ubuntu and verify again.

---

## 31. Security Notes

- Never commit `.env` files.
- Never commit local certificates or private keys.
- Never commit PostgreSQL passwords, JWT secrets, API keys, `.ppk`, `.pem`, or `.pfx` files.
- Keep FastAPI bound to `127.0.0.1` behind Nginx.
- Expose only the CodeIgniter `public` directory.
- Do not use `chmod -R 777`.
- Do not expose PostgreSQL port `5432` or Redis port `6379` to the network.
- Local `mkcert` certificates are for development only and must never be used in QA or production.
- QA and production must use publicly trusted certificates, such as certificates managed through AWS Certificate Manager or Let's Encrypt.

---

## 32. Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 10 July 2026 | Initial local environment setup |
| 1.1 | 10 July 2026 | Added local domains, Windows hosts configuration, complete Nginx frontend/API configuration, and troubleshooting |
