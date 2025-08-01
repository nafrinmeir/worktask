from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder="templates", static_folder="static")

API_URL = "http://api:5001"

@app.route("/")
def index():
    return "Frontend is running. Try /<username> to see the dashboard."

@app.route("/<username>")
def dashboard(username):
    r = requests.get(f"{API_URL}/tasks/{username}")
    if r.status_code == 200:
        tasks = r.json()
    else:
        tasks = []
    return render_template("dashboard.html", tasks=tasks, user=username)
    
    
@app.route("/admin", methods=["GET", "POST"])
def admin():
    user_response = requests.get(f"{API_URL}/users")
    task_response = []

    if request.method == "POST":
        if request.form["action"] == "add_user":
            username = request.form["username"]
            requests.post(f"{API_URL}/users", json={"username": username})
        elif request.form["action"] == "add_task":
            title = request.form["title"]
            description = request.form["description"]
            assignee = request.form["assignee"].strip().lower()  # normalize
            requests.post(f"{API_URL}/tasks", json={
                "title": title,
                "description": description,
                "assignee": assignee
            })

    user_response = requests.get(f"{API_URL}/users")
    users = user_response.json() if user_response.status_code == 200 else []

    for user in users:
        r = requests.get(f"{API_URL}/tasks/{user['username']}")
        user["tasks"] = r.json() if r.status_code == 200 else []

    return render_template("admin.html", users=users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)