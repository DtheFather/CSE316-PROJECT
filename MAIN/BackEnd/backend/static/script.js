// Register User
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;

    const response = await fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    document.getElementById('registerMessage').textContent = data.message;
});

// Login User
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    document.getElementById('loginMessage').textContent = data.message;

    // Show file upload section after successful login
    if (response.ok) {
        document.getElementById('fileUploadSection').style.display = 'block';
    }
});

// Upload File
document.getElementById('fileUploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
    });

    const data = await response.json();
    document.getElementById('fileUploadMessage').textContent = data.message;
});