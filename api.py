from models import app, db, User
from flask import jsonify, request

@app.route("/")
def home():
  return jsonify(message="Welcome to my api")

@app.route("/users", methods=["GET", "POST"])
def user_index_create():
  if request.method == "GET":
    # get all users
    return jsonify([])
  if request.method == "POST":
    # create a user
    # print(request.form)
    # print(request.get_json())
    new_user = User(name=request.form["name"], email=request.form["email"], bio=request.form["bio"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user)


if __name__ == "__main__":
  app.run()