# Teste de Integração Google Sign-In com Flask

Este projeto é um teste de integração do Google Sign-In com o framework Flask. O objetivo principal é demonstrar como implementar o botão de login do Google e autenticar os usuários em uma aplicação web utilizando o Google Sign-In.

## Ferramentas Utilizadas

- Python 3.x
- Flask
- Google Sign-In
- PostgreSQL (Banco de Dados)

## Introdução

Este projeto tem como propósito exemplificar a integração do Google Sign-In em uma aplicação Flask. O Google Sign-In é uma maneira segura e prática de autenticar usuários em um aplicativo usando suas contas do Google.

## Rotas

### Rota: `/`

A rota raiz exibe a página de login, onde os usuários podem fazer login com o Google ou usar um formulário de login convencional.

### Rota: `/cadastro`

A rota de cadastro exibe um formulário onde os usuários podem se cadastrar na aplicação.

### Rota: `/login` (Método POST)

Esta rota processa o login do usuário com o Google Sign-In. Retorna informações do usuário autenticado.

### Rota: `/clientes` (Método GET)

Esta rota retorna uma lista de todos os clientes cadastrados na aplicação.

### Rota: `/clientes` (Método POST)

Esta rota permite adicionar um novo cliente ao banco de dados.

### Rota: `/clientes/<int:id>` (Métodos GET, PUT, DELETE)

Estas rotas permitem visualizar, atualizar e excluir informações de um cliente específico no banco de dados.

## Criação da Tabela de Clientes

Foi criada uma tabela chamada `clientes` no banco de dados PostgreSQL para armazenar as informações dos clientes. A estrutura da tabela é a seguinte:

```sql
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(100) NOT NULL
);
```

## Como criar um projeto com Google

No painel do projeto, selecione "APIs e serviços" > "Identidade de API".
Clique em "Configurar consentimento do OAuth" e siga as instruções para configurar informações básicas do aplicativo.
Após configurar o consentimento, retorne a "APIs e serviços" > "Credenciais".
Depois, clique em "Criar credenciais" e selecione "ID do cliente OAuth".
Escolha "Aplicativo da Web" como o tipo de aplicativo, em seguida crie um ID do Cliente.
Após criar o cliente, você receberá um ID do cliente. Guarde essas informações em um local seguro.
No painel do projeto, também é possível gerenciar as configurações avançadas, como as permissões do OAuth e outras opções relacionadas ao Google Sign-In.

## Integrar o Google Sign-In em Seu Projeto Web

No lado do cliente (front-end), inclua a biblioteca do Google Sign-In em sua página usando um script semelhante a:

```
<script src="https://accounts.google.com/gsi/client" async defer></script>
```

- Configure o botão de login do Google Sign-In e vincule-o a uma função de callback que será executada após o login bem-sucedido.

- Na função de callback, você receberá um objeto que contém informações sobre o usuário autenticado, incluindo o token de ID.

- Envie o token de ID para o servidor (back-end) para verificar a autenticidade e obter informações adicionais, se necessário.

## Configurar Rotas e Autenticação no Servidor

Configure rotas em seu servidor (usando Flask, por exemplo) para processar as solicitações de login do Google e autenticar os usuários.

No servidor, verifique o token de ID recebido do cliente usando a biblioteca apropriada (por exemplo, google-auth) para garantir sua autenticidade.

Se o token for válido, você pode usar as informações contidas nele para autenticar o usuário em seu aplicativo.

## Links Relevantes

- https://console.developers.google.com

- https://developers.google.com/identity/gsi/web/guides/overview?hl=pt-br