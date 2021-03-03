from models import app, db, User
from flask import jsonify, request

@app.route("/")
def home():
  return jsonify(message="Welcome to my api")

@app.route("/users", methods=["GET", "POST"])
def user_index_create():
  if request.method == "GET":
    # get all users
    users= User.query.all()
    results = [user.to_dict() for user in users]
    return jsonify(results)
  if request.method == "POST":
    # create a user
    # print(request.form)
    # print(request.get_json())
    new_user = User(name=request.form["name"], email=request.form["email"], bio=request.form["bio"])
    db.session.add(new_user)
    db.session.commit()
    print(new_user)
    return jsonify(new_user.to_dict())


if __name__ == "__main__":
  app.run()