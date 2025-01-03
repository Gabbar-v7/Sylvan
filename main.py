from dotenv import load_dotenv

from src.utils.pre_loader import config

# Load env variables
load_dotenv(config.get("application", "env_file"))

from src.flasky import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
