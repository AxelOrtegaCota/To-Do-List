// Variables para almacenar el estado de las tareas
let tasks = [];

// Función de Login
function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Simula la verificación del login (usuario: "admin", contraseña: "password")
    if (username === 'admin' && password === '123') {
        document.getElementById('login-section').classList.remove('active');
        document.getElementById('todo-section').classList.add('active');
    } else {
        document.getElementById('login-error').style.display = 'block';
    }
}

// Función para añadir una nueva tarea
function addTask() {
    const content = document.getElementById('new-task-content').value;
    const image = document.getElementById('new-task-image').files[0];
    const reader = new FileReader();

    if (!content) {
        alert("Debes escribir una tarea.");
        return;
    }

    // Cargar imagen (si existe)
    if (image) {
        reader.readAsDataURL(image);
        reader.onload = function (e) {
            const imageUrl = e.target.result;
            createTaskElement(content, imageUrl);
        };
    } else {
        createTaskElement(content, null);
    }

    // Limpiar los campos de entrada
    document.getElementById('new-task-content').value = '';
    document.getElementById('new-task-image').value = '';
}

// Función para crear el elemento de la tarea
function createTaskElement(content, imageUrl) {
    const taskId = tasks.length;
    const taskElement = document.createElement('li');
    taskElement.classList.add('task');

    // Elemento de la tarea con contenido y botones de edición/eliminar
    taskElement.innerHTML = `
        <input type="text" value="${content}" id="task-${taskId}" readonly>
        ${imageUrl ? `<img src="${imageUrl}" alt="Imagen de tarea">` : ''}
        <button onclick="editTask(${taskId})">Editar</button>
        <button onclick="deleteTask(${taskId})">Borrar</button>
    `;

    // Añadir la tarea al DOM
    document.getElementById('task-list').appendChild(taskElement);

    // Guardar la tarea en la lista de tareas
    tasks.push({ id: taskId, content: content, imageUrl: imageUrl });
}

// Función para editar una tarea
function editTask(taskId) {
    const taskInput = document.getElementById(`task-${taskId}`);
    if (taskInput.readOnly) {
        taskInput.readOnly = false;
        taskInput.focus();
    } else {
        // Guardar cambios en la tarea
        taskInput.readOnly = true;
        tasks[taskId].content = taskInput.value;
    }
}

// Función para eliminar una tarea
function deleteTask(taskId) {
    const taskElement = document.getElementById(`task-${taskId}`).parentElement;
    taskElement.remove();
    tasks = tasks.filter(task => task.id !== taskId); // Eliminar tarea de la lista
}

function showRegister() {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('register-section').style.display = 'block';
}

function showLogin() {
    document.getElementById('register-section').style.display = 'none';
    document.getElementById('login-section').style.display = 'block';
}

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Obtener los datos del usuario guardados en localStorage
    const storedUsername = localStorage.getItem('username');
    const storedPassword = localStorage.getItem('password');

    if (username === storedUsername && password === storedPassword) {
        alert("Inicio de sesión exitoso");
        document.getElementById('login-section').style.display = 'none';
        document.getElementById('todo-section').style.display = 'block';
    } else {
        document.getElementById('login-error').style.display = 'block';
    }
}

function register() {
    const regUsername = document.getElementById('reg-username').value;
    const regPassword = document.getElementById('reg-password').value;
    const regConfirmPassword = document.getElementById('reg-confirm-password').value;

    // Validación de contraseñas
    if (regPassword !== regConfirmPassword) {
        document.getElementById('register-error').textContent = 'Las contraseñas no coinciden';
        document.getElementById('register-error').style.display = 'block';
        return;
    }

    // Guardar los datos en localStorage
    localStorage.setItem('username', regUsername);
    localStorage.setItem('password', regPassword);

    alert("Registro exitoso. Ahora puedes iniciar sesión.");

    // Cambiar a la vista de login
    showLogin();

}