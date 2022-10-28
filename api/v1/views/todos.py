#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Todos """

from models.todo import Todo
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response


@app_views.route('/todos', methods=['GET'], strict_slashes=False)
def all_todos():
    """ returns list of all todo objects """
    all_todos = []
    todos = storage.all(Todo).values()
    for todo in todos:
        d = todo.to_dict()
        del d['_sa_instance_state']
        print(d)
        all_todos.append(d)
    return jsonify(all_todos)


@app_views.route('/users/<user_id>/todos', methods=['GET'], strict_slashes=False)
def get_todos(user_id):
    """ returns list of all todo objects """

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    todos = []
    all_todos = storage.all(Todo).values()
    for todo in all_todos:
        d = todo.to_dict()
        del d['_sa_instance_state']
        if todo.user_id == user_id:
            todos.append(d)
    return jsonify(todos)


@app_views.route('/todos/<todo_id>', methods=['GET'], strict_slashes=False)
def get_todo(todo_id):
    """ returns list of all todo objects """
    todo = storage.get(Todo, todo_id)

    if not todo:
        abort(404)

    t = todo.to_dict()
    del t['_sa_instance_state']
    print(t)
    return jsonify(t)


@app_views.route('/todos/<todo_id>', methods=['DELETE'], strict_slashes=False)
def delete_todo(todo_id):
    """ delete a todo object """
    todo = storage.get(Todo, todo_id)

    if not todo:
        abort(404)

    todo.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>/todos', methods=['POST'], strict_slashes=False)
def create_todos(user_id):
    """ Creates a todo objects """
    data = request.get_json()

    print(data)
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    todo = Todo(data)
    todo.user_id = user_id
    for k, v in data.items():
        setattr(todo, k, v)
    todo.save()
    t = todo.to_dict()
    del t['_sa_instance_state']

    return jsonify(t), 201


@app_views.route('/todos/<todo_id>', methods=['PUT'], strict_slashes=False)
def update_todo(todo_id):
    """ delete a todo object """
    todo = storage.get(Todo, todo_id)

    if not todo:
        abort(404)

    data = request.get_json()

    if not data:
        return make_response(jsonify({"error": "Not a valid JSON"}), 400)

    for k, v in data.items():
        if k != 'id' and k != 'user_id' and k != 'created_at' and k != 'updated_at':
            setattr(todo, k, v)
    todo.save()
    t = todo.to_dict()
    del t['_sa_instance_state']

    return jsonify(t), 200
