from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from flask_bcrypt import Bcrypt
import io

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ""

db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)
bcrypt = Bcrypt(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    rated = db.Column(db.String(20), nullable=False)
    released_on = db.Column(db.Date(), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    plot = db.Column(db.String(4000), nullable=False)
    
    def __init__(self, title, year, rated, released_on, genre, director, plot):
        self.title = title
        self.year = year
        self.rated = rated
        self.released_on = released_on
        self.genre = genre
        self.director = director
        self.plot = plot
        
class MovieSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "year", "rated", "released_on", "genre", "director", "plot")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/movie/add", methods=["POST"])
def movie_add():
    post_data = request.get_json()
    title = post_data.get("title")
    year = post_data.get("year")
    rated = post_data.get("rated")
    released_on = post_data.get("realesed_on")
    genre = post_data.get("genre")
    director = post_data.get("director")
    plot = post_data.get("plot")
    

    new_movie = Movie(title, year, rated, released_on, genre, director, plot)
    db.session.add(new_movie)
    db.session.commit()

    return jsonify("Movie added")
    
@app.route("/movies/get", methods=["GET"])
def get_movies_data():
    movies_data = db.session.query(Movie).all()
    return jsonify(movies_schema.dump(movies_data))

@app.route("/movie/get/<id>", methods=["GET"])
def get_movie(id):
    movie_data = db.session.query(Movie).filter(Movie.id == id).first()
    return jsonify(movie_data)

@app.route("/movie/delete/<id>", methods=["DELETE"])
def delete_movie(id):
    movie_data = db.session.query(Movie).filter(Movie.id == id).first()
    db.session.delete(movie_data)
    db.session.commit()
    return jsonify("Movie Deleted")

@app.route("/movie/update/<id>", methods=["PUT"])
def update_movie(id):
    movie_data = db.session.query(Movie).filter(Movie.id == id).first()
    db.session.put(movie_data)
    db.session.commit()
    return jsonify("Movie updated")

@app.route("/user/add", methods=["POST"])
def create_user():
    if request.content_type != "application/json":
        return jsonify("Error")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    username_check = db.session.query(User.username).filter(User.username == username).first()
    if username_check is not None:
        return jsonify("Username taken")

    hashed_password = bcrypt.generate_password_hash(password).decode("utf8")

    record = User(username, hashed_password)
    db.session.add(record)
    db.session.commit()

    return jsonify("User created")

@app.route("/user/login", methods=["POST"])
def verify_user():
    if request.content_type != "application/json":
        return jsonify("Error, data must be sent as json")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    stored_password = db.session.query(User.password).filter(User.username == username).first()
    print(stored_password)
    print(password)

    if stored_password is None:
        return jsonify("User not Verified")

    valid_password_check = bcrypt.check_password_hash(stored_password[0], password)

    if valid_password_check == False:
        return jsonify("User not Verified")

    return jsonify("User verified")

if __name__ == "__main__":
    app.run(debug=True)