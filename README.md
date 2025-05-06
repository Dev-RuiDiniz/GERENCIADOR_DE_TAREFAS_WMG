
# 🗂️ Gestor de Tarefas WMG

Um sistema web simples de gerenciamento de tarefas com funcionalidades específicas para serviços, garantia e controle de entregas. Desenvolvido com **Flask** e **SQLite**, permite adicionar, editar, concluir, entregar e excluir tarefas com acompanhamento de prazos.

---

## 🚀 Funcionalidades

- ✅ Cadastro de tarefas com data de entrega
- 🛠️ Marcação de tarefas como "Garantia"
- 📦 Separação entre tarefas **pendentes**, **concluídas**, **entregues** e **com garantia**
- ⏰ Aviso de tarefas **atrasadas** ou com **prazo próximo**
- 🗃️ Histórico de tarefas entregues
- ✏️ Edição e exclusão de tarefas
- 🔒 Chave secreta para mensagens seguras com Flash
- 📋 Interface simples com Bootstrap (via templates HTML)

---

## 🧰 Tecnologias Utilizadas

- [Python 3](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [SQLite](https://www.sqlite.org/index.html)
- [Bootstrap 5](https://getbootstrap.com/)

---

## 🏗️ Estrutura de Pastas

```
gestor_wmg/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── adicionar_tarefa.html
│   ├── editar_tarefa.html
│   ├── garantia.html
│   ├── prontos.html
│   └── historico.html
├── models.py
├── app.py
└── README.md
```

---

## ⚙️ Como Executar Localmente

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/gestor-tarefas-wmg.git
   cd gestor-tarefas-wmg
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install flask flask_sqlalchemy
   ```

4. **Execute o sistema**
   ```bash
   python app.py
   ```

5. Acesse em seu navegador:
   ```
   http://127.0.0.1:5000/
   ```

---

## 🔐 Configuração de Segurança

- A chave secreta está definida como `'sua_chave_secreta_aqui'`.
- **Importante:** troque essa chave por algo seguro para produção.

```python
app.secret_key = 'minha_chave_super_secreta_123'
```

---

## 📌 Observações

- As tarefas são classificadas por:
  - **Serviço comum**
  - **Garantia**
  - **Declinadas (visuais apenas, não removem do sistema)**
- O sistema usa `flash` para alertar sobre prazos e ações executadas.
- Não possui autenticação de usuários (para sistemas com múltiplos usuários, adicione `Flask-Login` ou outro método).

---

## 🛠️ Melhorias Futuras

- Autenticação e autorização de usuários
- Filtros e busca por nome, data ou status
- Exportação de tarefas (CSV ou PDF)
- Responsividade mobile aprimorada
- Painel com gráficos de desempenho (ex: tarefas entregues por mês)

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Sinta-se à vontade para usar e modificar.
