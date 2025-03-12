# Podman Setup Guide

This guide explains how to set up **Podman** for running PostgreSQL and the **Sylvan Backend**.

## Install Podman

For Debian/Ubuntu:

```bash
sudo apt update && sudo apt install podman -y
```

For Fedora:

```bash
sudo dnf install podman -y
```

For Arch Linux:

```bash
sudo pacman -S podman
```

## Running PostgreSQL with Podman

```bash
podman run -d \
  --name sylvan-db \
  -e POSTGRES_USER=username \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=database_name \
  -v /absolute/path:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres
```

## Building and Running the Backend with Podman

1. **Build the Container Image:**
   Create a container specific configuration `container.ini`. Refer [docs/config.ini](ini-config.md)

   ```bash
   podman build -t sylvan-backend .
   ```

2. **Run the Application:**

   ```bash
   podman run  -p 5000:5000 --env-file env.development sylvan-backend:latest
   ```

3. **Verify Running Containers:**
   ```bash
   podman ps
   ```

API can be accessed at [`http://127.0.0.1:5000`](http://127.0.0.1:5000)
