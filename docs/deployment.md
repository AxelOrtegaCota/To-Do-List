# Deployment Guide


## Prerequisites
1. Ensure you have a database set up.
2. Obtain Google OAuth credentials (Client ID and Client Secret).
3. Configure environment variables:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`


## Deployment Steps
1. Clone the repository:
   ```bash
   git clone https://https://github.com/AxelOrtegaCota/To-Do-List
   cd todo-app

2. Install dependencies:
    pip install -r requirements.txt

3. Deploy to Render:
    - Set environment variables in Render's dashboard.
    - Use the following startCommand:
        gunicorn app:create_app()


## Troubleshooting
- Error: no such table: users
    Ensure you've run the database migrations using flask db upgrade.

- OAuth Errors:
    Verify that GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are correctly set in your environment variables.

