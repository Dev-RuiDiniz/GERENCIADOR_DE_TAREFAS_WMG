from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
from models import db, Tarefa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sua_chave_secreta_aqui'  # Substitua por uma chave segura em produção

db.init_app(app)

with app.app_context():
    db.create_all()

# Rota principal
@app.route('/')
def index():
    tarefas = Tarefa.query.filter_by(concluida=False).order_by(Tarefa.data_entrega).all()
    hoje = date.today()

    for tarefa in tarefas:
        if hasattr(tarefa, 'verificar_prazo'):
            status = tarefa.verificar_prazo()
            if status == "atrasada":
                flash(f'Tarefa "{tarefa.nome}" está ATRASADA!', 'danger')
            elif status == "proximo":
                flash(f'Tarefa "{tarefa.nome}" está com prazo próximo (2 dias ou menos)', 'warning')

    return render_template('index.html', tarefas=tarefas, hoje=hoje)

# Adicionar tarefa
@app.route('/adicionar_tarefa', methods=['GET', 'POST'])
def adicionar_tarefa():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        data_entrega_str = request.form.get('data_entrega', '')

        if not nome:
            flash('O nome da tarefa é obrigatório.', 'danger')
            return redirect(url_for('adicionar_tarefa'))

        try:
            data_entrega = date.fromisoformat(data_entrega_str)  # Usando apenas a parte de data
            if data_entrega < date.today():
                flash('A data de entrega não pode ser no passado!', 'danger')
                return redirect(url_for('adicionar_tarefa'))
        except ValueError:
            flash('Formato de data inválido. Use YYYY-MM-DD.', 'danger')
            return redirect(url_for('adicionar_tarefa'))

        nova_tarefa = Tarefa(nome=nome, descricao=descricao, data_entrega=data_entrega)

        try:
            db.session.add(nova_tarefa)
            db.session.commit()
            flash('Tarefa adicionada com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception:
            db.session.rollback()
            flash('Erro ao adicionar tarefa.', 'danger')

    return render_template('adicionar_tarefa.html')

# Concluir tarefa
@app.route('/concluir_tarefa/<int:tarefa_id>')
def concluir_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    tarefa.concluida = True
    tarefa.data_conclusao = date.today()  # Usando apenas a parte de data

    try:
        db.session.commit()
        flash('Serviço marcado como concluído e movido para o histórico!', 'success')
    except Exception:
        db.session.rollback()
        flash('Erro ao concluir tarefa.', 'danger')

    return redirect(url_for('index'))

# Rota para tarefas com garantia
@app.route('/garantia')
def garantias():
    garantias = Tarefa.query.filter_by(garantia=True).order_by(Tarefa.data_entrega).all()
    return render_template('garantia.html', garantias=garantias)

# Rota para tarefas prontas (concluídas, mas não entregues)
@app.route('/prontos')
def prontos():
    tarefas_prontas = Tarefa.query.filter(Tarefa.concluida == True, Tarefa.entregue == False).order_by(Tarefa.data_conclusao.desc()).all()
    return render_template('prontos.html', tarefas=tarefas_prontas)

# Rota para histórico (concluídas e entregues)
@app.route('/historico')
def historico():
    tarefas_concluidas = Tarefa.query.filter_by(concluida=True, entregue=True).order_by(Tarefa.data_conclusao.desc()).all()
    
    historico = []

    for tarefa in tarefas_concluidas:
        historico.append({
            'tipo': 'servico',
            'id': tarefa.id,
            'nome': tarefa.nome,
            'data_criacao': tarefa.data_criacao,
            'data_entrega': tarefa.data_entrega,
            'data_conclusao': tarefa.data_conclusao,
            'status': tarefa.status_entrega() if hasattr(tarefa, 'status_entrega') else '',
            'dias_realizacao': (tarefa.data_conclusao - tarefa.data_criacao).days
        })

    historico.sort(key=lambda x: x['data_conclusao'], reverse=True)
    return render_template('historico.html', historico=historico)

# Excluir tarefa
@app.route('/excluir_tarefa/<int:id>', methods=['POST'])
def excluir_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)

    try:
        db.session.delete(tarefa)
        db.session.commit()
        flash('Tarefa excluída com sucesso.', 'success')
    except Exception:
        db.session.rollback()
        flash('Erro ao excluir tarefa.', 'danger')

    return redirect(url_for('prontos'))

@app.route('/tarefa/<int:tarefa_id>/entregue', methods=['POST'])
def marcar_entregue(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    tarefa.entregue = True
    db.session.commit()
    flash('Tarefa marcada como entregue com sucesso!', 'success')
    return redirect(request.referrer or url_for('historico'))

# Editar tarefa
@app.route('/editar_tarefa/<int:tarefa_id>', methods=['GET', 'POST'])
def editar_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        data_entrega_str = request.form.get('data_entrega', '')

        if not nome:
            flash('O nome da tarefa é obrigatório.', 'danger')
            return redirect(url_for('editar_tarefa', tarefa_id=tarefa.id))

        try:
            nova_data = date.fromisoformat(data_entrega_str)  # Usando apenas a parte de data
            if nova_data < date.today():
                flash('A data de entrega não pode ser no passado!', 'danger')
                return redirect(url_for('editar_tarefa', tarefa_id=tarefa.id))
            tarefa.data_entrega = nova_data
        except ValueError:
            flash('Formato de data inválido. Use YYYY-MM-DD.', 'danger')
            return redirect(url_for('editar_tarefa', tarefa_id=tarefa.id))

        tarefa.nome = nome
        tarefa.descricao = descricao

        try:
            db.session.commit()
            flash('Tarefa atualizada com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception:
            db.session.rollback()
            flash('Erro ao atualizar tarefa.', 'danger')

    return render_template('editar_tarefa.html', tarefa=tarefa)

@app.route('/test')
def test():
    return 'Flask está funcionando!'

# Inicializador
if __name__ == '__main__':
    app.run(debug=True)
