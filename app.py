import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from main import emitir_certificado, ver_certificados, ver_saldo, transferir_token, queimar_token  # funções do main.py

app = Flask(__name__)
app.secret_key = 'segredo_seguro_aqui'

# Simulação de banco de dados de usuários
USUARIOS = {
    "admin": {"senha": "admin", "papel": "admin", "endereco": "0x3Ea3704bb6747A5175229666f01940A04893698b", "chave_privada": "084da8a88d1f87cf8df31165dea5bba9da4a5e28f0368c62a0884ac0a5821cb3"},
    "123285": {"senha": "12345", "papel": "aluno", "endereco": "0x3Ea3704bb6747A5175229666f01940A04893698b", "chave_privada": "084da8a88d1f87cf8df31165dea5bba9da4a5e28f0368c62a0884ac0a5821cb3"},
    "122274": {"senha": "12345", "papel": "aluno", "endereco": "0x2E53850f71d23D1f66bf49b9Bb6c6D656367a2f4", "chave_privada": "12ca037a42c54fd6cbc99c520313d312a32e84e8ea2c64c85b07b9d186d0d7a4"},
}

@app.route('/', methods=['GET', 'POST'])
def index():
    certificados = []
    if request.method == 'POST':
        aluno = request.form['aluno']
        try:
            certificados = ver_certificados(aluno)
        except Exception as e:
            flash(f'❌ Erro: {str(e)}', 'danger')
    return render_template('index.html', certificados=certificados)

@app.route('/login', methods=['POST'])
def login():
    # Limpa mensagens de flash pendentes
    session.pop('_flashes', None)
    
    usuario = request.form['usuario']
    senha = request.form['senha']
    user_data = USUARIOS.get(usuario)

    if user_data and user_data['senha'] == senha:
        session['usuario'] = usuario
        session['papel'] = user_data['papel']
        flash('✅ Login realizado com sucesso!', 'success')
        if user_data['papel'] == 'admin':
            return redirect(url_for('dashboard_admin'))
        elif user_data['papel'] == 'aluno':
            return redirect(url_for('dashboard_aluno'))
    else:
        flash('❌ Usuário ou senha inválidos.', 'danger')
        return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
    session.clear()
    flash('✅ Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard/admin', methods=['GET', 'POST'])
def dashboard_admin():
    if session.get('papel') != 'admin':
        flash('❌ Acesso negado.', 'danger')
        return redirect(url_for('index'))

    endereco = USUARIOS[session['usuario']]['endereco']
    certificados = []

    if request.method == 'POST':
        aluno = request.form['aluno']
        try:
            certificados = ver_certificados(aluno)
            if not certificados:
                flash('❌ Nenhum certificado encontrado para este aluno.', 'danger')
        except Exception as e:
            flash(f'❌ Erro ao buscar certificados: {str(e)}', 'danger')

    try:
        saldo = ver_saldo(endereco)  # Recalcula o saldo ao carregar a página
        return render_template('dashboard_admin.html', saldo=saldo, certificados=certificados)
    except Exception as e:
        flash(f"❌ Erro ao buscar saldo: {str(e)}", 'danger')
        return redirect(url_for('index'))

@app.route('/dashboard/aluno', methods=['GET', 'POST'])
def dashboard_aluno():
    if session.get('papel') != 'aluno':
        flash('❌ Acesso negado.', 'danger')
        return redirect(url_for('index'))

    endereco = USUARIOS[session['usuario']]['endereco']
    certificados = []

    if request.method == 'POST':
        try:
            certificados = ver_certificados(endereco)
            if not certificados:
                flash('❌ Nenhum certificado encontrado.', 'danger')
        except Exception as e:
            flash(f'❌ Erro ao buscar certificados: {str(e)}', 'danger')

    try:
        saldo = ver_saldo(endereco)  # Recalcula o saldo ao carregar a página
        return render_template('dashboard_aluno.html', saldo=saldo, certificados=certificados)
    except Exception as e:
        flash(f"❌ Erro ao buscar saldo: {str(e)}", 'danger')
        return redirect(url_for('index'))

@app.route('/emitir', methods=['POST'])
def emitir():
    aluno = request.form['aluno']
    nome = request.form['nome']
    curso = request.form['curso']
    data = request.form['data']
    id_cert = request.form['id_cert']
    try:
        emitir_certificado(aluno, nome, curso, data, id_cert)
        flash('✅ Certificado emitido com sucesso!', 'success')
    except Exception as e:
        flash(f'❌ Erro ao emitir certificado: {str(e)}', 'error')
    return redirect(url_for('dashboard_admin'))

@app.route('/aluno', methods=['GET'])
def aluno():
    if 'usuario' not in session or session['papel'] != 'aluno':
        print(f"Usuário não está logado ou não é aluno.")
        flash('❌ Você precisa estar logado como aluno para acessar esta funcionalidade.', 'danger')
        return redirect(url_for('index'))

    endereco = USUARIOS[session['usuario']]['endereco']
    try:
        certs = ver_certificados(endereco)
        return render_template('aluno.html', certificados=certs)
    except Exception as e:
        flash(f"❌ Erro ao buscar certificados: {str(e)}", 'danger')
        return redirect(url_for('dashboard_aluno'))

@app.route('/verificar')
def verificar():
    # (Simples: lista todos os certificados públicos. Pode melhorar depois.)
    return redirect(url_for('aluno'))

@app.route('/saldo', methods=['GET'])
def saldo():
    if 'usuario' not in session:
        flash('❌ Você precisa estar logado para acessar esta funcionalidade.', 'danger')
        return redirect(url_for('index'))

    endereco = USUARIOS[session['usuario']]['endereco']
    try:
        tokens = ver_saldo(endereco)
        print("Saldo:", tokens)
        return render_template('saldo.html', saldo=tokens)
    except Exception as e:
        print("Erro ao consultar saldo:", e)
        flash(f"Erro ao consultar saldo: {str(e)}", "danger")
        return redirect(url_for('dashboard_' + session['papel']))

@app.route('/transferir', methods=['POST'])
def transferir():
    if 'usuario' not in session:
        flash('❌ Você precisa estar logado para acessar esta funcionalidade.', 'danger')
        return redirect(url_for('index'))

    usuario = session['usuario']
    user_data = USUARIOS.get(usuario)

    if not user_data:
        flash('❌ Usuário não encontrado.', 'danger')
        return redirect(url_for('index'))

    destinatario = request.form['destinatario']
    quantidade = int(request.form['quantidade'])
    chave_privada = user_data['chave_privada']  # Obtém a chave privada do usuário logado

    try:
        transferir_token(chave_privada, destinatario, quantidade)
        flash('✅ Transferência realizada com sucesso!', 'success')
    except Exception as e:
        flash(f'❌ Erro ao transferir CTK: {str(e)}', 'error')

    # Redirecionar para o dashboard correto com base no papel do usuário
    if session['papel'] == 'admin':
        return redirect(url_for('dashboard_admin'))
    elif session['papel'] == 'aluno':
        return redirect(url_for('dashboard_aluno'))

@app.route('/queimar', methods=['POST'])
def queimar():
    aluno = request.form['aluno']
    quantidade = int(request.form['quantidade'])
    chave_privada_admin = os.getenv("CHAVE_PRIVADA")  # Obtém a chave privada do admin do .env

    try:
        queimar_token(chave_privada_admin, aluno, quantidade)
        flash('🔥 Tokens queimados com sucesso!', 'success')
    except Exception as e:
        print(f"Erro ao queimar CTK: {e}")
        flash(f'❌ Erro ao queimar CTK: {str(e)}', 'error')

    return redirect(url_for('dashboard_admin'))


if __name__ == '__main__':
    app.run(debug=True)
