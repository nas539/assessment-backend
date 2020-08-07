from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from flask_bcrypt import Bcrypt
import io

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://axsgcanmprtycq:2c1bc41c2445028e5c0b8bbd85041320e43975615fb7aac90887e97646017e2b@ec2-34-200-15-192.compute-1.amazonaws.com:5432/d3mjgenn8a0rf9"

db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)
bcrypt = Bcrypt(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    # Example: PG-13
    rated = db.Column(db.String(20), nullable=False)
    released_on = db.Column(db.Date(), nullable=False)
    genre = db.Column(db.String(40), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    plot = db.Column(db.String(3000), nullable=False)
    rating = db.Column(db.Integer(), nullable=True)
    count = db.Column(db.Integer(), nullable=True)
    
    def __init__(self, title, year, rated, released_on, genre, director, plot, rating, count):
        self.title = title
        self.year = year
        self.rated = rated
        self.released_on = released_on
        self.genre = genre
        self.director = director
        self.plot = plot
        self.rating = rating
        self.count = count

class MovieSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "year", "rated", "released_on", "genre", "director", "plot", "rating", "count")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@app.route("/movie/add", methods=["POST"])
def movie_add():
    if rquest.content_type != "application.json":
        return jsonify("Error")

    post_data = request.get_json()
    title = post_data.get("title")
    year = post_data.get("year")
    rated = post_data.get("rated")
    released_on = post_data.get("realesed_on")
    genre = post_data.get("genre")
    director = post_data.get("director")
    plot = post_data.get("plot")

    return jsonify("Movie added")
    
@app.route("/movies/get", methods=["GET"])
def get_movies_data():
    movies_data = db.session.query(Movie).all()
    return jsonify(movies_schema.dump(movies_data))

if __name__ == "__main__":
    app.run(debug=True)