# Sylvan Backend

A **Flask-based web API** utilizing **SQLAlchemy** for database management and **JWT Tokens** for user authentication.

## Features

- **User Authentication:** Secure login/logout functionality.
- **Database Integration:** SQLAlchemy ORM for seamless interactions.
- **Security Measures:** CSRF protection, session management, and encryption.

---

## Getting Started

### Prerequisites

- Python **3.12.8** (recommended)
- Podman with PostgreSQL image:
  ```bash
  podman pull docker.io/postgres
  ```

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Gabbar-v7/Sylvan.git
   cd Sylvan
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv env
   ```

3. **Activate the Virtual Environment:**

   - **Windows:**
     ```bash
     env\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source env/bin/activate
     ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Configuration Files:**

   - **[`env.development`](docs/env-config.md)** – Contains sensitive information such as API keys and database credentials.
   - **[`config.ini`](docs/ini-config.md)** – Stores general configuration settings.

6. **Run PostgreSQL via Podman:**

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

7. **Start the Application:**

   ```bash
   python main.py
   ```

8. **Access the API:**
   - Open your browser and visit: `http://127.0.0.1:5000`

---

## Podman Configuration

To containerize the project using **Podman**, follow these steps:

1. **Build the Container Image:**
   Create a container specific configuration `container.ini`. Refer [docs/config.ini](docs/ini-config.md)

   ```bash
   podman build -t sylvan-backend .
   ```

2. **Run the Application in a Container:**

   ```bash
   podman run  -p 5000:5000 --env-file env.development sylvan-backend:latest
   ```

3. **Verify Running Containers:**

   ```bash
   podman ps
   ```

4. **Access the Application:**
   - Visit [`http://127.0.0.1:5000`](http://127.0.0.1:5000)

For detailed **Podman setup**, refer to **[`Podman Setup`](docs/podman-setup.md)**.

---

## File Structure

```
Root/
├── src/
│   ├── dbModels/
│   ├── flasky/
│   ├── security/
│   └── utils/
├── scripts/
├── settings/
├── temp/
├── docs/
├── Containerfile
├── .containerignore
├── .gitignore
├── README.md
├── LICENSE
├── main.py
└── requirements.txt
```

---

## Contributing

1. **Fork the Repository:**

   ```bash
   git fork https://github.com/Gabbar-v7/Sylvan.git
   ```

2. **Create a Feature Branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Your Changes:**

   ```bash
   git commit -m "Your concise commit message"
   ```

4. **Push the Branch:**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Submit a Pull Request on GitHub.**

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Additional Notes

For issues or feature requests, open a new [Issue](https://github.com/Gabbar-v7/Sylvan/issues).
