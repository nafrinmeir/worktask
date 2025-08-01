from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")
db = client["TaskListTest"]
tasks = db["AllTaskTest"]
users = db["Users"]

@app.route("/")
def index():
    return "API is running. Use /users, /tasks or /tasks/<username>."

# ---------------- USERS ----------------
@app.route("/users", methods=["GET"])
def list_users():
    all_users = list(users.find())
    for u in all_users:
        u["_id"] = str(u["_id"])
    return jsonify(all_users)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if not data.get("username"):
        return jsonify({"error": "username required"}), 400
    if users.find_one({"username": data["username"]}):
        return jsonify({"error": "user already exists"}), 409
    result = users.insert_one({"username": data["username"]})
    return jsonify({"_id": str(result.inserted_id)}), 201

@app.route("/users/<username>", methods=["DELETE"])
def delete_user(username):
    users.delete_one({"username": username})
    tasks.delete_many({"assignee": username})
    return '', 204

# ---------------- TASKS ----------------
@app.route("/tasks/<username>", methods=["GET"])
def get_tasks(username):
    user_tasks = list(tasks.find({"assignee": username}))
    for task in user_tasks:
        task["_id"] = str(task["_id"])
    return jsonify(user_tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    assignee = data.get("assignee", "").strip().lower()
    if not assignee or not users.find_one({"username": assignee}):
        return jsonify({"error": "Invalid or missing assignee"}), 400
    data["assignee"] = assignee  # normalize
    result = tasks.insert_one(data)
    return jsonify({"_id": str(result.inserted_id)}), 201


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    result = tasks.delete_one({"_id": ObjectId(task_id)})
    return ("", 204) if result.deleted_count else ("Not Found", 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
