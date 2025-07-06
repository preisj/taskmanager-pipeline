from flask import Blueprint, request, jsonify
from app import db
from app.models import Task

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': t.id, 'description': t.description, 'status': t.status} for t in tasks])

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'description' not in data:
        return jsonify({'error': 'Descrição obrigatória'}), 400
    task = Task(description=data['description'], status=data.get('status', 'Pendente'))
    db.session.add(task)
    db.session.commit()
    return jsonify({'message': 'Tarefa criada', 'id': task.id}), 201

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({'message': 'Tarefa atualizada'})

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Tarefa removida'})
