from flask import Flask, request, jsonify, abort
from models import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify([{'id': t.id, 'title': t.title, 'done': t.done} for t in Task.query.all()])

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title'):
        abort(400)
    task = Task(title=data['title'])
    db.session.add(task); db.session.commit()
    return jsonify({'id': task.id}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    t = Task.query.get_or_404(task_id)
    data = request.get_json()
    t.title = data.get('title', t.title)
    t.done = data.get('done', t.done)
    db.session.commit()
    return '', 204

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    t = Task.query.get_or_404(task_id)
    db.session.delete(t); db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
