
<h1 align="center"><strong>To-Do App</strong> 📝</h1>
<p align="center"> 
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white" alt="Python"/> 
  <img src="https://img.shields.io/badge/Flask-2.1+-lightgrey?logo=flask&logoColor=black" alt="Flask"/> 

</p> <p align="center"> A modern, minimalistic To-Do List application built with <strong>Flask</strong>, complete with user authentication, task management, and a robust testing pipeline. </p>

<h2>✨ Features</h2>
    <ul>
        <li><strong>🛡️ Secure:</strong> Fully functional user authentication system.</li>
        <li><strong>📝 Intuitive:</strong> Create, read, update, and delete tasks with ease.</li>
        <li><strong>🌐 RESTful API:</strong> Programmatically manage tasks via endpoints.</li>
        <li><strong>🧪 Tested:</strong> Comprehensive test coverage ensures stability.</li>
    </ul>

  <hr/>

  <h2>📖 Table of Contents</h2>
  <ul>
      <li><a href="#installation">Installation</a></li>
      <li><a href="#usage">Usage</a></li>
      <li><a href="#api-documentation">API Documentation</a></li>
      <li><a href="#testing">Testing</a></li>
      <li><a href="#contributing">Contributing</a></li>
      <li><a href="#credits">Credits</a></li>
  </ul>

  <hr/>

  <h2 id="installation">🚀 Installation</h2>
  <ol>
      <li><strong>Clone the repository:</strong>
          <pre><code>git clone https://github.com/username/todo-app.git
cd todo-app</code></pre>
      </li>
      <li><strong>Set up a virtual environment:</strong>
          <pre><code>python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate</code></pre>
      </li>
      <li><strong>Install dependencies:</strong>
          <pre><code>pip install -r requirements.txt</code></pre>
      </li>
      <li><strong>Set up the database:</strong>
          <pre><code>flask db upgrade</code></pre>
      </li>
      <li><strong>Run the app locally:</strong>
          <pre><code>flask run</code></pre>
      </li>
  </ol>

  <hr/>

  <h2 id="usage">🎯 Usage</h2>
  <h3>Web Interface</h3>
  <ul>
      <li><strong>Login/Register:</strong> <code>/auth/login</code> and <code>/auth/register</code></li>
      <li><strong>Manage Tasks:</strong> <code>/tasks</code></li>
  </ul>

  <h3>RESTful API</h3>
  <ul>
      <li><strong>Get all tasks:</strong> <code>GET /api/tasks</code></li>
      <li><strong>Create a task:</strong> <code>POST /api/tasks</code></li>
      <li><strong>Update a task:</strong> <code>PUT /api/tasks/&lt;id&gt;</code></li>
      <li><strong>Delete a task:</strong> <code>DELETE /api/tasks/&lt;id&gt;</code></li>
  </ul>

  <hr/>

  <h2 id="api-documentation">📜 API Documentation</h2>
  <table>
      <thead>
          <tr>
              <th><strong>Endpoint</strong></th>
              <th><strong>Method</strong></th>
              <th><strong>Description</strong></th>
          </tr>
      </thead>
      <tbody>
          <tr>
              <td><code>/api/tasks/</code></td>
              <td>GET</td>
              <td>Retrieve all tasks</td>
          </tr>
          <tr>
              <td><code>/api/tasks/</code></td>
              <td>POST</td>
              <td>Create a new task</td>
          </tr>
          <tr>
              <td><code>/api/tasks/&lt;id&gt;</code></td>
              <td>PUT</td>
              <td>Update a specific task</td>
          </tr>
          <tr>
              <td><code>/api/tasks/&lt;id&gt;</code></td>
              <td>DELETE</td>
              <td>Delete a specific task</td>
          </tr>
      </tbody>
  </table>

  <hr/>

  <h2 id="testing">🧪 Testing</h2>
  <ol>
      <li><strong>Run all tests:</strong>
          <pre><code>pytest</code></pre>
      </li>
      <li><strong>Check coverage:</strong>
          <pre><code>pytest --cov=app</code></pre>
      </li>
  </ol>

  <hr/>

  <h2 id="contributing">🤝 Contributing</h2>
  <ol>
      <li><strong>Fork this repository.</strong></li>
      <li><strong>Create a new branch:</strong>
          <pre><code>git checkout -b feature-name</code></pre>
      </li>
      <li><strong>Commit your changes:</strong>
          <pre><code>git commit -m "Add feature-name"</code></pre>
      </li>
      <li><strong>Push your branch and submit a pull request.</strong></li>
  </ol>

  <hr/>

  <h2 id="credits">📄 Credits</h2>
  <p align="center">Made by Axel Patricio Ortega Cota</p>
