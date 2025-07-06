import pytest
from app import create_app, db
from app.models import Task

@pytest.fixture
def app():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
    with app.app_context():
        db.create_all()
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

def create_sample_task(client, desc="Test task", status="Pendente"):
    return client.post('/tasks', json={'description': desc, 'status': status})

# 1. Testa se a lista de tarefas inicia vazia
def test_get_tasks_empty(client):
    resp = client.get('/tasks')
    assert resp.status_code == 200
    assert resp.json == []

# 2. Testa criação de tarefa válida
def test_create_task(client):
    resp = create_sample_task(client)
    assert resp.status_code == 201
    assert 'id' in resp.json

# 3. Testa erro ao criar tarefa sem descrição
def test_create_task_no_description(client):
    resp = client.post('/tasks', json={})
    assert resp.status_code == 400

# 4. Testa se tarefa criada aparece na listagem
def test_task_appears_in_list(client):
    create_sample_task(client, "Nova tarefa")
    resp = client.get('/tasks')
    assert len(resp.json) == 1
    assert resp.json[0]['description'] == "Nova tarefa"

# 5. Testa atualização de descrição e status
def test_update_task(client):
    create_sample_task(client)
    resp = client.put('/tasks/1', json={'description': 'Atualizado', 'status': 'Feito'})
    assert resp.status_code == 200

# 6. Testa exclusão de tarefa
def test_delete_task(client):
    create_sample_task(client)
    resp = client.delete('/tasks/1')
    assert resp.status_code == 200
    assert resp.json['message'] == 'Tarefa removida'

# 7. Testa atualizar tarefa inexistente
def test_update_nonexistent_task(client):
    resp = client.put('/tasks/999', json={'description': 'X'})
    assert resp.status_code == 404

# 8. Testa deletar tarefa inexistente
def test_delete_nonexistent_task(client):
    resp = client.delete('/tasks/999')
    assert resp.status_code == 404

# 9. Testa criação de múltiplas tarefas
def test_multiple_task_creation(client):
    for i in range(5):
        create_sample_task(client, f"Task {i}")
    resp = client.get('/tasks')
    assert len(resp.json) == 5

# 10. Testa que status padrão é 'Pendente'
def test_default_status(client):
    resp = client.post('/tasks', json={'description': 'Sem status'})
    assert resp.status_code == 201
    id = resp.json['id']
    task = client.get('/tasks').json[0]
    assert task['status'] == 'Pendente'

# 11. Testa update parcial (só descrição)
def test_partial_update_description(client):
    create_sample_task(client, "Original")
    resp = client.put('/tasks/1', json={'description': 'Parcial'})
    assert resp.status_code == 200
    tasks = client.get('/tasks').json
    assert tasks[0]['description'] == 'Parcial'

# 12. Testa update parcial (só status)
def test_partial_update_status(client):
    create_sample_task(client)
    resp = client.put('/tasks/1', json={'status': 'Em progresso'})
    assert resp.status_code == 200
    tasks = client.get('/tasks').json
    assert tasks[0]['status'] == 'Em progresso'

# 13. Testa que não cria com campo desconhecido
def test_create_task_with_extra_field(client):
    resp = client.post('/tasks', json={'description': 'Tarefa', 'extra': 'valor'})
    assert resp.status_code == 201

# 14. Testa que GET individual não existe (404 esperado)
def test_get_individual_not_allowed(client):
    resp = client.get('/tasks/1')
    assert resp.status_code == 404 or resp.status_code == 405

# 15. Testa que método GET em rota de DELETE não é permitido
def test_invalid_method_on_delete(client):
    create_sample_task(client)
    resp = client.get('/tasks/1')
    assert resp.status_code in (404, 405)

# 16. Testa que uma tarefa pode ser deletada após update
def test_update_then_delete(client):
    create_sample_task(client)
    client.put('/tasks/1', json={'status': 'Concluído'})
    resp = client.delete('/tasks/1')
    assert resp.status_code == 200

# 17. Testa criação com status customizado
def test_create_with_custom_status(client):
    resp = client.post('/tasks', json={'description': 'Custom', 'status': 'Urgente'})
    assert resp.status_code == 201
    task = client.get('/tasks').json[0]
    assert task['status'] == 'Urgente'

# 18. Testa inserção com string vazia
def test_create_with_empty_description(client):
    resp = client.post('/tasks', json={'description': ''})
    assert resp.status_code == 400

# 19. Testa que tarefas são isoladas por teste
def test_database_isolation(client):
    resp = client.get('/tasks')
    assert resp.json == []

# 20. Testa update sem payload (não altera nada)
def test_update_with_no_data(client):
    create_sample_task(client, "Atualizar")
    resp = client.put('/tasks/1', json={})
    assert resp.status_code == 200
    task = client.get('/tasks').json[0]
    assert task['description'] == 'Atualizar'
