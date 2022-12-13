from jogoteca import app
from flask import Flask, render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form = FormularioUsuario(request.form)

    proxima = 'index' if request.form['proxima'] else request.form['proxima']

    user = Usuarios.query.filter_by(nickname = form.nickname.data).first()
    senha = check_password_hash(user.senha, form.senha.data)
    
    if user and senha:
        session['usuario'] = user.nickname
        flash(session['usuario']+' logado com sucesso!')
        return redirect(url_for(proxima))
    else:
        flash('Usuário Não Logado!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario'] = None
    flash('Logout realizado!')
    return redirect(url_for('index'))