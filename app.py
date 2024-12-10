from flask import Flask, jsonify
from flask_mail import Mail, Message
import mysql.connector
import os
from dotenv import load_dotenv
import traceback

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Usando variável de ambiente "email"
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Usando variável de ambiente "senha do email"
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME') # Usando variável de ambiente
mail = Mail(app)

# Conexão com o banco de dados MySQL
def banco_de_dados():
    conexão = mysql.connector.connect(
        host='localhost',
        user='root',
        password=os.getenv('DB_PASSWORD'), # Usando variável do .env
        database='natal_db'
    )
    return conexão

# Rota para enviar os e-mails
@app.route('/enviar_feliz_natal', methods=['GET'])
def enviar_feliz_natal():
    try:
        # Me conectar ao banco de dados
        conectar = banco_de_dados()
        cursor = conectar.cursor(dictionary=True)
        
        # Obter os clientes
        cursor.execute("SELECT nome, email FROM clientes")
        clientes = cursor.fetchall()
        
        if not clientes:
            raise ValueError("Nenhum cliente encontrado no banco de dados.")

        # Enviar e-mail para cada cliente
        for cliente in clientes:
            msg = Message(
                'FELIZ NATAL!',
                recipients=[cliente['email']]
            )
            msg.body = f"Olá {cliente['nome']},\n\nNeste Natal, queremos expressar nossa gratidão por sua confiança e parceria ao longo deste ano. Que esta época seja repleta de alegria, paz e momentos especiais ao lado de quem você ama. Feliz Natal e um próspero Ano Novo!\n\nAtenciosamente,\nÉkodex S.A"
            try:
                mail.send(msg)
                print(f'E-mail enviado para {cliente["nome"]} ({cliente["email"]})')
            except Exception as e:
                print(f'Erro ao enviar e-mail para {cliente["nome"]}: {e}')
                print(traceback.format_exc())
        
        cursor.close()
        conectar.close()
        return jsonify({'message': 'E-mails enviados com sucesso!'})

    except Exception as e:
        print(f'Ocorreu um erro ao tentar enviar os e-mails: {e}')
        print(traceback.format_exc())  # Log detalhado
        return jsonify({'message': 'Erro ao enviar os e-mails'}), 500

if __name__ == '__main__':
    app.run(debug=True)
    
    