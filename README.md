# Sylvan-Backend

A Flask-based web API utilizing SQLAlchemy for database management and JWT Tokens for user authentication.

## Features

- **User Authentication:** Login and logout functionality.
- **Database Integration:** SQLAlchemy ORM for seamless database interactions.
- **Secure Application:** CSRF protection, session management, and encryption.

## Getting Started

### Prerequisites

- Recommended Python version: **3.12.8**
- Podman with PostgreSQL image:
  ```bash
  podman pull postgres
  ```

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Gabbar-v7/Sylvan.git
   cd Sylvan
   ```

2. Create a virtual environment:

   ```bash
   python -m venv env
   ```

3. Activate the virtual environment:

   - **Windows:**
     ```bash
     env\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source env/bin/activate
     ```

4. Install dependencies:

   - **Windows:**

   ```bash
   pip install -r requirements-win.txt
   ```

   - **Mac/Linux:**

   ```bash
   pip install -r requirements-linux.txt
   ```

5. Set up configuration files:

   #### `env.development` (for sensitive environment variables):

   This file should only contain sensitive information such as API keys, database credentials, and encryption keys.

   ```plaintext
   SQLALCHEMY_DATABASE_URI="postgresql://{dbUserName}:{dbPassword}@localhost:5432/{dbDataSet}"

   FLASK_SESSION_KEY="your_secure_session_key"

   HASH_KEY="your_secret_hash_key"

   FERNET_KEY=b"bwN8yS9PbEx1yEDCQQ8R2qfioZFR2vKEtDuRslWjJUU="  # Fernet key must be 32 URL-safe base64-encoded bytes.

   # Visit: https://console.cloud.google.com/
   GOOGLE_CLIENT_ID = ""
   GOOGLE_CLIENT_SECRET = ""

   # Visit: https://developers.facebook.com/
   FACEBOOK_CLIENT_ID=""
   FACEBOOK_CLIENT_SECRET=""
   ```

   #### `config.ini` (for general configurations):

   This file contains references to other configuration files or general settings.

   ```plaintext
   [application]
   env_file=env.development
   enable_traceback=true

   [database]
   echo=false
   max_overflow = 10
   pool_timeout = 30
   ```

6. Run PostgreSQL via Podman:

   ```bash
   podman run -d \
     --name sylvan \
     -e POSTGRES_USER={dbUserName} \
     -e POSTGRES_PASSWORD={dbPassword} \
     -e POSTGRES_DB={dbDataSet} \
     -v {absolute_path}:/var/lib/postgresql/data \
     -p 5432:5432 \
     postgres
   ```

7. Start the application:

   ```bash
   python main.py
   ```

8. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## Usage

- Login with your credentials or register as a new user (if registration is implemented).
- Interact with application features such as managing resources and viewing content.

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
├── podman/                # Folder for all Podman-related files
│   ├── Containerfile      # Container configuration file
│   ├── podman-compose.yml # Podman Compose file
│   └── podman-config/     # Additional Podman configs
├── .gitignore
├── README.md
├── LICENSE
├── main.py
└── requirements.txt
```

---

## Contributing

1. Fork the repository:

   ```bash
   git fork https://github.com/Gabbar-v7/Sylvan.git
   ```

2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Commit your changes:

   ```bash
   git commit -m "Your concise commit message"
   ```

4. Push your branch:

   ```bash
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request on GitHub.

**Note:** Use the `temp/` directory for experimental work. it is ignored by Git.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

### Additional Notes

For any issues or feature requests, create a new [issue](https://github.com/Gabbar-v7/Sylvan/issues) in the repository.
