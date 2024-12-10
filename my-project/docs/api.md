# API Documentation


## Endpoints


### Authentication Endpoints
1. **Register**
   - **Endpoint:** `/auth/register`
   - **Method:** POST
   - **Description:** Registers a new user.
   - **Request Body Example (JSON):**
     ```json
     {
       "username": "exampleuser",
       "email": "example@example.com",
       "password": "password123"
     }
     ```
   - **Response Example:**
     ```json
     {
       "message": "User successfully registered"
     }
     ```

2. **Login**
   - **Endpoint:** `/auth/login`
   - **Method:** POST
   - **Description:** Logs in an existing user.
   - **Request Body Example (JSON):**
     ```json
     {
       "username": "exampleuser",
       "password": "password123"
     }
     ```
   - **Response Example:**
     ```json
     {
       "message": "Welcome exampleuser"
     }
     ```

3. **Logout**
   - **Endpoint:** `/auth/logout`
   - **Method:** GET
   - **Description:** Logs out the current user.
   - **Response Example:**
     ```json
     {
       "message": "Logged out successfully"
     }
     ```


### Task Management Endpoints
1. **Get All Tasks**
   - **Endpoint:** `/tasks`
   - **Method:** GET
   - **Description:** Retrieves all tasks for the current user.

2. **Create Task**
   - **Endpoint:** `/tasks`
   - **Method:** POST
   - **Description:** Creates a new task.
   - **Request Body Example (JSON):**
     ```json
     {
       "title": "New Task",
       "description": "This is a new task"
     }
     ```

3. **Update Task**
   - **Endpoint:** `/tasks/<task_id>`
   - **Method:** PUT
   - **Description:** Updates a task by ID.
   - **Request Body Example (JSON):**
     ```json
     {
       "title": "Updated Task",
       "description": "This is the updated task"
     }
     ```

4. **Delete Task**
   - **Endpoint:** `/tasks/<task_id>`
   - **Method:** DELETE
   - **Description:** Deletes a task by ID.


### Joke Fetching Endpoint
1. **Fetch Random Joke**
   - **Endpoint:** `/jokes/joke`
   - **Method:** GET
   - **Description:** Fetches a random joke.
   - **Response Example:**
     ```json
     {
       "type": "single",
       "joke": "Why don't programmers like nature? It has too many bugs."
     }
     ```


### OAuth Endpoints
1. **Google Login**
   - **Endpoint:** `/oauth/login`
   - **Method:** GET
   - **Description:** Initiates Google OAuth login flow.

2. **Google Callback**
   - **Endpoint:** `/oauth/callback`
   - **Method:** GET
   - **Description:** Handles the callback from Google OAuth.
