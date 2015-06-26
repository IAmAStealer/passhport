# -*-coding:Utf-8 -*-
import os

from nose.tools import *
from sqlalchemy import exc

from app            import app, db
from app.models_mod import user
from config         import basedir

class TestUser:
    """Test for the class User"""
    @classmethod
    def setup_class(cls):
        """Initialize configuration and create an empty database before testing"""
        app.config['TESTING']                 = True
        app.config['WTF_CSRF_ENABLED']        = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "test.db")
        cls.app                               = app.test_client()
        db.create_all()

    @classmethod
    def teardown_class(cls):
        """Delete the database created for testing"""
        db.session.remove()
        db.drop_all()

    def setUp(self):
        """Does nothing"""
        pass

    def tearDown(self):
        """Rollback after raising a database exception for testing"""
        db.session.rollback()
        db.session.flush()

    def test_create(self):
        """User creation in database succeeds"""
        email   = "john@example.com"
        sshkey  = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com"""
        comment = "This is a great comment"
        output  = """Email: john@example.com\nSSH key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com\nComment: This is a great comment"""

        u = user.User(email = email, sshkey = sshkey, comment = comment)

        db.session.add(u)
        db.session.commit()

        assert_equal(u.email, email)
        assert_equal(u.sshkey, sshkey)
        assert_equal(u.comment, comment)
        assert_equal(repr(u), output)

    @raises(exc.IntegrityError)
    def test_create_existing_email(self):
        """User creation in database with an already used email fails"""
        email   = "john@example.com"
        sshkey  = """ssh-rsa AAAAB3NzEaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john2@example.com"""
        comment = "A random comment man"

        u = user.User(email = email, sshkey = sshkey, comment = comment)

        db.session.add(u)
        db.session.commit()

    @raises(exc.IntegrityError)
    def test_create_existing_sshkey(self):
        """User creation in database with an already used sshkey fails"""
        email   = "john3@example.com"
        sshkey  = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com"""
        comment = "An awesome comment man"

        u = user.User(email = email, sshkey = sshkey, comment = comment)

        db.session.add(u)
        db.session.commit()

    # We should test if an empty email while creating a user raises an error, but it seems that SQLite doesn't check it
    # def test_create_empty_email(self):

    # We should test if an empty sshkey while creating a user raises an error, but it seems that SQLite doesn't check it
    # def test_create_empty_sshkey(self):

    def test_edit(self):
        """User edition in database succeeds"""
        email       = "example@test.org"
        sshkey      = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT example@test.org"""
        comment     = "That comment"
        new_email   = "oh@yeah.net"
        new_sshkey  = """A short key"""
        new_comment = "A new comment"

        u = user.User(email = email, sshkey = sshkey, comment = comment)

        db.session.add(u)
        db.session.commit()

        user_to_edit = db.session.query(user.User).filter_by(email = "example@test.org")

        user_to_edit.update({"email": "bla".encode("utf8"), "sshkey": new_sshkey.encode("utf8"), "comment": new_comment.encode("utf8")})
        db.session.commit()
