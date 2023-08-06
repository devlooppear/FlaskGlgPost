from flask import request, jsonify, render_template
from app import app
from app.database import connect
import json
import jwt
from google.auth.transport import requests
from google.oauth2 import id_token
YOUR_GOOGLE_CLIENT_ID ='<seu_client_id>'
def autenticar_cliente(token):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), YOUR_GOOGLE_CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Token de emissão inválido.')
        return True
    except ValueError:
        return False
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/cadastro', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({"mensagem": "Token é obrigatório."}), 400

    try:
        # Verificar a validade do token usando a biblioteca do Google
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), YOUR_GOOGLE_CLIENT_ID)

        # Verificar se o token foi emitido para o seu aplicativo
        if idinfo['aud'] != YOUR_GOOGLE_CLIENT_ID:
            raise ValueError('Token de emissão inválido.')

        # Se tudo estiver correto, retornar as informações do usuário autenticado
        return jsonify({
            "name": idinfo.get('name'),
            "sub": idinfo.get('sub'),
            "given_name": idinfo.get('given_name'),
            "family_name": idinfo.get('family_name'),
            "email": idinfo.get('email'),
            "email_verified": idinfo.get('email_verified'),
            "picture": idinfo.get('picture')
        }), 200
    except ValueError as e:
        return jsonify({"mensagem": "Token inválido ou cliente não autenticado."}), 401
# Rota para lidar com o cadastro do cliente
@app.route('/clientes', methods=['POST'])
def handle_clientes():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    if not nome or not email or not senha:
        return jsonify({"mensagem": "Por favor, preencha todos os campos."}), 400

    conn = connect()
    if not conn:
        return jsonify({"mensagem": "Erro ao conectar ao banco de dados."}), 500

    try:
        # Verificar se o email já existe no banco de dados
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM clientes WHERE email=%s", (email,))
            existing_client = cursor.fetchone()
            if existing_client:
                return jsonify({"mensagem": "Email já registrado."}), 422
            cursor.execute("INSERT INTO clientes (nome, email, senha) VALUES (%s, %s, %s) RETURNING id",
                           (nome, email, senha))
            novo_id = cursor.fetchone()[0]
            conn.commit()
            return jsonify({"mensagem": "Cliente adicionado com sucesso.", "id": novo_id}), 201
    except Exception as e:
        print(f"Erro ao adicionar cliente: {e}")
        conn.rollback()
        return jsonify({"mensagem": "Erro ao adicionar cliente no banco de dados."}), 500
    finally:
        conn.close()
@app.route('/clientes', methods=['GET'])
def get_all_clientes():
    conn = connect()
    if not conn:
        return jsonify({"mensagem": "Erro ao conectar ao banco de dados."}), 500

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nome, email FROM clientes")
            clientes = cursor.fetchall()

            return jsonify({"clientes": clientes}), 200
    except Exception as e:
        print(f"Erro ao buscar clientes: {e}")
        return jsonify({"mensagem": "Erro ao buscar clientes no banco de dados."}), 500
    finally:
        conn.close()
@app.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    conn = connect()
    if not conn:
        return jsonify({"mensagem": "Erro ao conectar ao banco de dados."}), 500
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nome, email FROM clientes WHERE id=%s", (id,))
            cliente = cursor.fetchone()

            if cliente:
                return json.dumps({"cliente": cliente}, ensure_ascii=False).encode('utf-8'), 200, {'Content-Type': 'application/json; charset=utf-8'}
            else:
                return jsonify({"mensagem": "Cliente não encontrado."}), 404
    except Exception as e:
        print(f"Erro ao buscar cliente: {e}")
        return jsonify({"mensagem": "Erro ao buscar cliente no banco de dados."}), 500
    finally:
        conn.close()
@app.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    conn = connect()
    if not conn:
        return jsonify({"mensagem": "Erro ao conectar ao banco de dados."}), 500
    try:
        data = request.get_json()
        nome = data.get('nome')
        email = data.get('email')

        with conn.cursor() as cursor:
            cursor.execute("UPDATE clientes SET nome=%s, email=%s WHERE id=%s", (nome, email, id))
            conn.commit()
            return jsonify({"mensagem": "Cliente atualizado com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao atualizar cliente: {e}")
        conn.rollback()
        return jsonify({"mensagem": "Erro ao atualizar cliente no banco de dados."}), 500
    finally:
        conn.close()
@app.route('/clientes/<int:id>', methods=['DELETE'])
def excluir_cliente(id):
    conn = connect()
    if not conn:
        return jsonify({"mensagem": "Erro ao conectar ao banco de dados."}), 500
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM clientes WHERE id=%s", (id,))
            conn.commit()
            return jsonify({"mensagem": "Cliente excluído com sucesso."}), 200
    except Exception as e:
        print(f"Erro ao excluir cliente: {e}")
        conn.rollback()
        return jsonify({"mensagem": "Erro ao excluir cliente no banco de dados."}), 500
    finally:
        conn.close()