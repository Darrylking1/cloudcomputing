from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
import os

app = Flask(__name__)

# Redis setup
r = redis.Redis(host="redis", port=6379)

# PostgreSQL setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

# Define a simple model for demonstration
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visit_count = db.Column(db.Integer, nullable=False)

# Home route with Redis counter
@app.route("/")
def home():
    count = r.incr("hits")
    return f"This page has been visited {count} times."

# New route to store and retrieve visit count in PostgreSQL
@app.route("/pg")
def pg_home():
    # Check if a record exists, if not, create it
    visit = Visit.query.first()
    if visit is None:
        visit = Visit(visit_count=1)
        db.session.add(visit)
    else:
        visit.visit_count += 1
    
    db.session.commit()
    return f"PostgreSQL visit count: {visit.visit_count}"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
