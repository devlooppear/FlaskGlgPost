const YOUR_GOOGLE_CLIENT_ID = '<seu_client_id>'

function onSignIn(data) {
    if (!data || !data.credential) {
        console.error('Erro ao fazer login: Usuário não encontrado.');
        return;
    }

    var idToken = data.credential;

    // Fetch the user information from the backend using the received token
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ token: idToken })
    })
    .then(response => response.json())
    .then(data => {
        // Exibir informações do usuário autenticado
        document.getElementById('fullName').textContent = data.name;
        document.getElementById('sub').textContent = data.sub;
        document.getElementById('given_name').textContent = data.given_name;
        document.getElementById('family_name').textContent = data.family_name;
        document.getElementById('email').textContent = data.email;
        document.getElementById('verifiedEmail').textContent = data.email_verified;
        document.getElementById('picture').setAttribute('src', data.picture);

        // Verificar se o e-mail está na lista de clientes
        const email = data.email;
        fetch('/clientes')
        .then(response => response.json())
        .then(clientesData => {
            const clientes = clientesData.clientes;
            const foundClient = clientes.find(cliente => cliente[2] === email);

            if (foundClient) {
                // Exibir alerta de login bem-sucedido
                alert('Login realizado com sucesso!');
            }

            // Exibir a div com informações do usuário autenticado
            document.getElementById('userInfo').style.display = 'block';
        });
    })
    .catch(error => {
        console.error('Erro ao fazer login:', error);
    });
}


// Inicialização do Google Sign-In
function initializeGoogleSignIn() {
    const clientID = YOUR_GOOGLE_CLIENT_ID;

    google.accounts.id.initialize({
        client_id: clientID,
        callback: onSignIn // Use the onSignIn function as the callback
    });

    google.accounts.id.renderButton(
        document.getElementById('google-signin-button'),
        {
            theme: 'filled_black',
            size: 'big',
            type: 'standard',
            shape: 'pill',
            locale: 'pt-BR',
            logo_alignment: 'left'
        }
    );

    google.accounts.id.prompt(); // also display the One Tap dialog
}

// Call the initialization function on window.onload
window.onload = initializeGoogleSignIn;
