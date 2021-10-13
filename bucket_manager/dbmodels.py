from bucket_manager import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Access_id = db.Column(db.String(100), unique=True, nullable=False)
    Access_key = db.Column(db.String(100), unique=True, nullable=False)
    