# Environment Configuration

This file contains the required environment variables for running the **Sylvan Backend**.

## Required Variables

Create a file named `env.development` in the project root and add the following variables:

```ini
# Database
SQLALCHEMY_DATABASE_URI = postgresql://{dbUserName}:{dbPassword}@localhost:5432/{dbDataSet}

#Flask
FLASK_SESSION_KEY = your_secure_session_key
HASH_KEY = your_secret_hash_key
FERNET_KEY = b"bwN8yS9PbEx1yEDCQQ8R2qfioZFR2vKEtDuRslWjJUU="  # Fernet key must be 32 URL-safe base64-encoded bytes.

# OAuth
# Visit: https://console.cloud.google.com/
GOOGLE_CLIENT_ID =
GOOGLE_CLIENT_SECRET =
# Visit: https://developers.facebook.com/
FACEBOOK_CLIENT_ID =
FACEBOOK_CLIENT_SECRET =
```

**Note:**

- Replace the placeholders with actual values.
- Keep this file secure as it contains sensitive information.
