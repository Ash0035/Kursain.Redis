from flask import Flask, render_template, request, redirect
import redis

app = Flask(__name__)
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

@app.route("/")
def index():
    counter = r.get("counter") or 0
    saved_value = r.get("saved_value") or ""
    items = r.lrange("items", 0, -1)
    return render_template("index.html", counter=counter, saved_value=saved_value, items=items)

@app.route("/save", methods=["POST"])
def save_value():
    value = request.form["value"]
    r.set("saved_value", value)
    return redirect("/")

@app.route("/increment")
def increment():
    r.incr("counter")
    return redirect("/")

@app.route("/add_item", methods=["POST"])
def add_item():
    item = request.form["item"]
    r.lpush("items", item)
    return redirect("/")

@app.route("/reset")
def reset_all():
    r.delete("counter")
    r.delete("saved_value")
    r.delete("items")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
