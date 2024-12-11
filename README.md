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
- **Integrated Chat System**: Real-time chat feature integrated within the app.
- **Minimal Server Requests**: Optimized architecture for reduced load on the server.  

---

## Getting Started  

To get started with **Sylvan**, follow the steps below to set up the environment and install dependencies.

### Prerequisites  
 - **Python:** 3.12.8 recomended

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
   ```bash  
   pip install -r requirements.txt  
   ```  

5. Set up the `keys.py` file in the root directory and define the following variables:  
   ```python  
   # keys.py
   SQLALCHEMY_DATABASE_URI = "postgresql://{dbUserName}:{dbPassword}@localhost:5432/{dbDataSet}"

   FLASK_SESSION_KEY = "your_secure_session_key"

   HASH_KEY = "your_secret_hash_key"

   FERNET_KEY = b"bwN8yS9PbEx1yEDCQQ8R2qfioZFR2vKEtDuRslWjJUU="   # Fernet key must be 32 url-safe base64-encoded bytes. Ref: https://cryptography.io/en/latest/fernet/#cryptography.fernet.Fernet
   ```  

6. Run Postgres via Docker:  (Optionally use any other SQL Database)
   ```bash
   docker run -d \
   --name homeogenie \
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

## Usage  
- Login with your credentials or register as a new user (if registration is implemented).  
- Interact with the app features, such as managing resources and viewing content.  

---

## File Structure  
```  
Root/  
├── src/  
│   ├── dbModels/         # SQLAlchemy definitions  
│   ├── flasky/           # Flask setup, including CORS, LoginManager, etc   
│   └── security/          # Security code like hashing and encryption
│ 
├── scripts/              # Essential scripts  
├── .gitignore  
├── README.md  
├── LICENSE               # MIT License
├── main.py               # Main entry point for the app  
└── requirements.txt      # Dependencies  
 
```  

---

## Contributing  
1. Fork the repository.  
2. Create a feature branch: `git checkout -b category/tag`.  
3. Commit your changes: `git commit -m "{message}"`.  
4. Push to the branch: `git push origin category/tag`.  
5. Create a Pull Request on GitHub.  

**Note:** For rough work use temp/ folder in Root directory. It is ignored by git.

---

## License  
This project is licensed under the [MIT License](LICENSE).  

---

### Additional Notes  
For any issues, create a new [issue](https://github.com/Gabbar-v7/Sylvan/issues) in the repository.
