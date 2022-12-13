from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo
import time

# Index
@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos = lista)

# New Game
@app.route('/novo')
def novo():
    if 'usuario' not in session or session['usuario'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)

# Function Create
@app.route('/criar', methods=['POST',])
def criar():

    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    jogo = Jogos.query.filter_by(nome = nome).first()

    if jogo:
        flash('Jogo já criado!')
        return redirect(url_for('index'))
    
    new_game = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(new_game)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']

    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{new_game.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

# Edit Game
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario' not in session or session['usuario'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = Jogos.query.filter_by(id=id).first()

    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa_jogo = recupera_imagem(id)

    return render_template('editar.html', titulo='Editando Jogo', id=id, capa_jogo=capa_jogo, form=form)

# Function Create
@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():

        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']

        timestamp = time.time()
        deleta_arquivo(jogo.id)
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario' not in session or session['usuario'] == None:
        return redirect(url_for('login'))
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo excluído com sucesso!')

    return redirect(url_for('index'))




@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads',nome_arquivo)

