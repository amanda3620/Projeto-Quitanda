from flask import Flask, render_template, request,redirect, session
import sqlite3 as sql
import uuid

app = Flask(__name__)
app.secret_key = "quitandazezinho"

# Nome e senha para entrar no site como administrador
usuario = "Seu_zé"
senha = "8765"
# Caso um dos dois ou ambos estiverem errado não entrará, por isso o false
login = False

# Verificar a sessão do arquivo (login)
def verifica_sessao():
    if "login" in session and session['login']:
        return True
    else :
        return False

# Verificar o database, ou seja os dados conectados ao arquivo sql
def conecta_database():
    conexao = sql.connect("db_quitanda.db")
    conexao.row_factory = sql.Row
    return conexao

# Iniciar o arquivo sql
def iniciar_db():
    conexao = conecta_database()
    with app.open_resource('esquema.sql', mode='r') as comandos:
        conexao.cursor().executescript(comandos.read())
    conexao.commit()
    conexao.close()

# rota para a página home
@app.route("/")
def index():
    iniciar_db()
    conexao = conecta_database()
    # Quando clicar em um produto ele será identificado pelo id 
    produtos = conexao.execute('SELECT * FROM produtos ORDER BY id_prod DESC').fetchall()
    conexao.close()
    # Onde na parte {{title}} do modelo, será trocada pelo nome Home, para mostrar que está na página home
    title = "Home"
    return render_template("home.html", produtos=produtos,title=title)


# Para finalizar a rota 
app.run(debug=True)
