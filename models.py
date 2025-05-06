from datetime import date, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #identificador único da tarefa
    nome = db.Column(db.String(100), nullable=False) #nome da tarefa
    descricao = db.Column(db.Text) #descrição da tarefa
    
    garantia = db.Column(db.Boolean, default=False) #se a tarefa é uma garantia
    declinada = db.Column(db.Boolean, default=False) #se a tarefa foi declinada

    data_criacao = db.Column(db.Date, default=date.today) #data de criação da tarefa
    data_entrega = db.Column(db.Date, nullable=False) #prazo de entrega da tarefa
    data_conclusao = db.Column(db.Date) #data de conclusão da tarefa

    concluida = db.Column(db.Boolean, default=False) #se a tarefa foi concluída
    

    def verificar_prazo(self):
        hoje = date.today()
        if self.concluida:
            return "concluída"
        elif self.data_entrega < hoje:
            return "atrasada"
        elif (self.data_entrega - hoje) <= timedelta(days=3):
            return "proximo"
        else:
            return "normal"

    def dias_para_entrega(self):
        hoje = date.today()
        if self.concluida:
            return (self.data_conclusao - self.data_criacao).days
        elif self.data_entrega < hoje:
            return (hoje - self.data_criacao).days
        else:
            return (self.data_entrega - hoje).days

    def status_entrega(self):
        if not self.concluida:
            return "pendente"
        return "no prazo" if self.data_conclusao <= self.data_entrega else "atrasada"
