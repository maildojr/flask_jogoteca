from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console

jogo1 = Jogo('Tetris','Puzzle','Atari')
jogo2 = Jogo('God of War','Rack n Slash','PS2')
jogo3 = Jogo('Mortal Kombat','Luta','PS2')
lista = [jogo1, jogo2, jogo3]

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome=nome
        self.nickname=nickname
        self.senha=senha

usuario1 = Usuario('Maildo Barros','maildojr','teste')
usuario2 = Usuario('Andréia Barros','andreia','teste')
usuario3 = Usuario('Luna Barros','luna','teste')
usuarios = {
    usuario1.nickname: usuario1,
    usuario2.nickname: usuario2,
    usuario3.nickname: usuario3
}

app = Flask(__name__)
app.secret_key = 'alura'


@app.route('/')
def index():
    if 'usuario' not in session or session['usuario'] == None:
        return redirect('/login')
    return render_template('lista.html', titulo='Jogos', jogos = lista)

@app.route('/novo')
def novo():
    if 'usuario' not in session or session['usuario'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    proxima = request.form['proxima']
    
    if usuario in usuarios:
        if senha == usuarios[usuario].senha:
            session['usuario'] = usuario
            flash(session['usuario']+' logado com sucesso!')
            return redirect(proxima)
    else:
        flash('Usuário Não Logado!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario'] = None
    flash('Logout realizado!')
    return redirect(url_for('login'))

app.run(debug=True)