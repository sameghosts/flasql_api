from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/flasql"
# [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]:/[DB_NAME]
db = SQLAlchemy(app)

# -------- MODELS ------
class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, unique=True, nullable=False)
  name = db.Column(db.String, nullable=False)
  bio = db.Column(db.String(150))

  posts = db.relationship("Post", back_populates="author", lazy=True)
  # posts = db.relationship("Post", backref="author", lazy=True)
  def __repr__(self):
    return f"User(id={self.id}, email={self.email}, name={self.name}, bio={self.bio})"

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "email": self.email,
      "bio": self.bio
    }
  
  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

post_tags = db.Table(
  "post_tags",
  db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
  db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)

class Post(db.Model):
  __tablename__ = "posts"

  id = db.Column(db.Integer, primary_key=True)
  header = db.Column(db.String(150), unique=True, nullable=False)
  body = db.Column(db.String, nullable=False)
  author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="SET NULL"))

  author = db.relationship("User", back_populates="posts", lazy="subquery")
  # author = db.relationship("User", backref="posts") - on back ref on needs to be on one model, with backpopulate you need on both and is more explicit
  tags = db.relationship("Tag", back_populates="posts", lazy="subquery", secondary=post_tags)

  def __repr__(self):
    return f"Post(id={self.id}, header={self.header}, body={self.body}, author_id={self.author_id}"

class Tag(db.Model):
  __tablename__ = "tags"

  id = db.Column(db.Integer, primary_key=True)
  tag = db.Column(db.String(50), unique=True, nullable=False)

  posts = db.relationship("Post", back_populates="tags", lazy=True, secondary=post_tags)


  def __repr__(self):
    return f"Tag(id={self.id}, tag={self.tag}"

