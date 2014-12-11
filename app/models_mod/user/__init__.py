from app import db

"""
    User defines informations for every adminsys using passhport
"""
class User(db.Model):
    
    id      = db.Column(db.Integer,     primary_key=True)
    username= db.Column(db.String(256), index=True,     unique=True,
                                                        nullable=False)
    email   = db.Column(db.String(120), index=True,     unique=True)
    sshkey  = db.Column(db.String(500), index=False,    unique=True,
                                                        nullable=False)
    comment = db.Column(db.String(500), index=True)

    def __repr__(self):
        return '<User %r>' % (self.name)

