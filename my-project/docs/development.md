# Development Guide


## Setting Up the Project
1. Clone the repository:
   ```bash
   git clone https://https://github.com/AxelOrtegaCota/To-Do-List
   cd todo-app

2. Create a virtual environment:
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt

4. Set up environment variables in a .env file:
    SECRET_KEY=your_secret_key
    DATABASE_URL=sqlite:///development.db
    GOOGLE_CLIENT_ID=your_google_client_id
    GOOGLE_CLIENT_SECRET=your_google_client_secret

5. Start the development server:
    flask run
