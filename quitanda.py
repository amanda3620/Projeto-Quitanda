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

# Rota de Login
@app.route("/login")
def login():
    # Onde na parte {{title}} do modelo, será trocada pelo nome Login, para mostrar que está na página login
    title="Login"
    return render_template("login.html", title=title)

#Rota para a página de acesso
@app.route("/acesso, methods=['post']")
def acesso():
    global usuario, senha
    usuario_informado = request.form["usuario"]
    senha_informada = request.form["senha"]
    if usuario == usuario_informado and senha == senha_informada:
        session["login"] = True
        return redirect("/adm")
    else:
        return
render_template("login.html", msg="Usuário/senha incorretos!")

# Rota da página ADM
@app.route("/adm")
def adm():
    if verifica_sessao():
        iniciar_db()
        conexao = conecta_database
        produtos = conexao.execute('SELECT * FROM produtos ORDER BY id_prod DESC').fetchall()
        conexao.close()
        title = "Administração"
        return render_template("adm.html", produtos=produtos, title=title)
    else:
        return redirect("/login")

# Rota de logout
@app.route("/logout")
def logout():
    global login 
    login = False
    session.clear()
    return redirect("/")

# Rota da página de cadastro
@app.route("/cadprodutos")
def cadprodutos():
    if verifica_sessao():
        title = "Cadastro de produtos"
        return render_template("cadprodutos.html", title=title)
    else:
        return redirect("/login")

# Rota da página de cadastro no banco
@app.route("/cadastro", methods=['post'])
def cadastro():
    if verifica_sessao():
        nome_prod=request.form['nome_prod']
        desc_prod=request.form['desc_prod']
        preco_prod=request.form['preco_prod']
        img_prod=request.files['img_prod']
        id_foto=str(uuid.uuid4().hex)
        filename=id_foto+nome_prod+'.png'
        img_prod.save("static/img/produtos/"+filename)
        conexao = conecta_database()
        conexao.execute('INSERT INTO produtos (nome_prod, desc_prod, preco_prod, img_prod) VALUES (?, ?, ?, ?)', (nome_prod, desc_prod, preco_prod, filename))
        conexao.commit()
        conexao.close()
        return redirect("/adm")
    else:
        return redirect("/login")

# Para finalizar a rota 
app.run(debug=True)
