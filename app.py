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



if __name__ == "__main__":
    app.run(debug=True)