from flask  import Flask, render_template, request, redirect, session, flash, url_for
from models import Jogo, Usuario

from dao import JogoDao
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'alura'

app.config['MYSQL_HOST'] = "127.0.0.1"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "20101993"
app.config['MYSQL_DB'] = "jogoteca"
app.config['MYSQL_PORT'] = 3306

db = MySQL(app)

jogo_dao = JogoDao(db)



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

	jogo_dao.salvar(jogo)
	return redirect(url_for('index'))




@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
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


app.run(debug=True)


