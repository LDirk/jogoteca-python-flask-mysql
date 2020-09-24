from flask  import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogo, Usuario
from dao import JogoDao, UsuarioDao
from flask_mysqldb import MySQL
import os 
import time 

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = MySQL(app)

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)



usuario1 = Usuario('lucas','Lucas Dirk','1234')
usuario2 = Usuario('Nico', 'Nico Steppat', '7a1')
usuario3 = Usuario('flavio', 'Flavio', 'javascript')

usuarios = {usuario1.id: usuario1, usuario2.id: usuario2, usuario3.id: usuario3}

jogo1 = Jogo('GTA V ', '/ Ação /', 'XBOX ONE')
jogo2 = Jogo('Final Fantasy XII', '/ RPG /', 'PS1')
jogo3 = Jogo('Ragnarok', '/ MMORPG /', 'PC')
lista = [jogo1, jogo2,jogo3] 

@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo='Meus Joguinhos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('novo')))
    return render_template('novo.html', titulo='Novo jogo')


@app.route('/criar', methods=['POST',])
def criar():


    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome,categoria,console)
    jogo = jogo_dao.salvar(jogo)
    arquivo = request.files['arquivo']

    upload_path = app.config['UPLOAD_PATH']


    timestamp = time.time()

    arquivo.save(f'{upload_path}/capa{jogo.id}--{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogo_dao.busca_por_id(id)

    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando jogo', jogo=jogo,capa_jogo = nome_imagem)


@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id=request.form['id'])
    jogo_dao.salvar(jogo)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()

    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
        
    jogo_dao.deletar(id)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST',])
def autenticar():

    usuario = usuario_dao.buscar_por_id(request.form['usuario'])

    if usuario :
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)

    else :
        flash('Não logado, tente de novo!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
	session['usuario_logado'] = None 
	flash('Nenhum usuario logado')
	return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):

    return send_from_directory('uploads', nome_arquivo)

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    os.remove(os.path.join(app.config['UPLOAD_PATH'],arquivo))


app.run(debug=True)


