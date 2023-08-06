document.getElementById('cadastroForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(document.getElementById('cadastroForm'));
    
    // Aqui você pode adicionar o token ao FormData
    // formData.append('token', 'seu_token_aqui');

    fetch('/clientes', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Aqui você pode lidar com a resposta do servidor, como exibir uma mensagem de sucesso
    })
    .catch(error => {
        console.error('Erro:', error);
        // Aqui você pode lidar com erros, como exibir uma mensagem de erro
    });
});