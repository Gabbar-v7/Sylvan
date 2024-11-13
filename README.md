
# Sylvan

Sylvan is a flexible and scalable Flask project template designed for seamless growth and easy maintenance. Built with a modular architecture using Blueprints, SQLAlchemy ORM, encryption, and hashing, Sylvan provides a strong foundation for web applications that require high performance and security. This template includes essential features like a real-time chat system and dynamic flashcards, which display various status messages, such as success, warning, error, info, and danger, to enhance user experience and feedback.

To ensure high performance and low latency, Sylvan optimizes server interactions by reducing the number of HTTP requests. Static assets like HTML, CSS, and JavaScript are bundled into a single file, streamlining page loads and reducing network overhead.

Whether you're building a small-scale app or a large enterprise solution, Sylvan’s architecture is designed to scale with your needs. The integrated features can easily be extended to accommodate new functionality as your project evolves.

## Features

- **Flask Blueprints**: Modular structure for scaling the application by separating concerns.
- **Encryption & Hashing**: Secure user authentication and sensitive data handling using industry-standard techniques.
- **SQLAlchemy ORM**: Simplifies interaction with the database and provides a convenient, Pythonic interface.
- **Flash Cards with Status**: Display messages to users with various status indicators, including success, warning, error, info, and danger.
- **Optimized Static Files**: Minimizes HTTP requests by combining HTML, CSS, and JavaScript into a single file.
- **Chat System**: Real-time chat feature integrated within the app.
- **Minimal Server Requests**: Optimized architecture for reduced load on the server.

## Installation

To get started with **Sylvan**, follow the steps below to set up the environment and install dependencies.

### 1. Clone the Repository

```bash
git clone https://github.com/Gabbar-v7/Sylvan.git
cd Sylvan
```

### 2. Set up a Virtual Environment

```bash
python3 -m venv .env
source .env/bin/activate  
# On Windows, use .env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Environment Variables/Keys

Create a `keys.py` file in the root directory and set the necessary variables:

```python
# keys.py Optionally connect them to environment variables

FLASK_SESSION_KEY = r"\U*/Iwpr#=HV"  # Random string
HASH_KEY = r"B9&ZYu+C;l*g"   # Random String 
FERNET_KEY = b"9iZ1K0sVZmA4K_I77xdJftE2qJ6Nwq1A7l9HjBM_APQ="    # Use cryptograpy.Fernet.generate_key() to generate new key

```

### 5. Run the Development Server

To run the application locally:

```bash
python main.py
```

Your app will be available at `http://127.0.0.1:5000/`.

## Project Structure

The project is organized in a modular and scalable way, leveraging Flask Blueprints for different components:

```
Sylvan/
│
├── .github/
│   └── templates/               # GitHub Actions templates
│
├── assets/                      # Project resources (e.g., images, design backups)
│
├── src/
│   ├── dbHandler/               # Database handler and ORM models
│   │   ├── __init__.py          # Initializes DB and session
│   │   └── dbUser.py            # User ORM model
│   │
│   ├── flasky/                  # Flask app components
│   │   ├── static/              # Static files (CSS, JS, images, etc.)
│   │   │   ├── images/          # Image assets
│   │   │   ├── script/          # JS scripts
│   │   │   ├── style/           # CSS styles
│   │   │   ├── svgs/            # SVGs
│   │   ├── templates/           # HTML templates
│   │   │   ├── components/      # Reusable components (e.g., chat, flashcards)
│   │   │   ├── error/           # Error pages (e.g., 400, 401, 403, 500)
│   │   │   ├── pages/           # Protected pages (login required)
│   │   │   ├── session/         # Session management (login/signup)
│   │   │   ├── base.html        # Base layout template
│   │   │   └── index.html       # Home page
│   │   ├── __init__.py          # App initialization and blueprint registration
│   │   ├── errors.py            # Error handling routes
│   │   ├── index.py             # Home page logic
│   │   ├── page.py              # Other page routes
│   │   └── session.py           # Session management logic
│   │
│   ├── security/                # Security measures
│   │   ├── oneway.py            # One-way security (e.g., hashing)
│   │   └── twoway.py               # Two-way security (e.g., encryption)
│   │
│   └── tools/                   # Utility scripts
│   
├── .gitignore                   # Git ignore file
├── DOCUMENTATION.md             # Complete Documentation
├── LICENSE.md                   # License information
├── README.md                    # Project README
├── keys.py                      # API keys or sensitive data (to be configured)
├── main.py                      # Main entry point to run the app
└── requirements.txt             # Project dependencies
```

### For more details checkout [DOCUMENTATION.md](DOCUMENTATION.md)

## Components

### 1. Chat System

A real-time chat system integrated with Flask and optimized for communication between users. This feature allows asynchronous chat functionality to enhance user experience.

### 2. Flashcards

Flashcards with different message types (success, warning, error, info, danger) to display relevant notifications to the user. They can be used for alerting users to different application states or outcomes.

### 3. Authentication

The authentication system includes secure hashing and encryption techniques for storing passwords. It uses Flask session management.

## Optimizations

- **Single Static File**: All CSS, JavaScript, and HTML files are combined into a single static file to minimize requests and improve performance.
- **Efficient Database Handling**: Utilizes SQLAlchemy ORM for optimized database queries and reduces unnecessary requests to the server.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details.

## Questions

If you have any questions or need further assistance, feel free to open a discussion. 

---

Happy coding with **Sylvan**!

