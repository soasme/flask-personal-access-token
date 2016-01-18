# -*- coding: utf-8 -*-

from datetime import datetime
from werkzeug.security import generate_password_hash
from .core import db

class PersonalAccessToken(db.Model):

    __tablename__ = 'personal_access_token'

    __table_args__ = (
        db.UniqueConstraint('token', name='ux_token'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(64), nullable=False)
    salt = db.Column(db.String(8), nullable=False)
    token = db.Column(db.String(40), nullable=False)
    scopes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime)

    def to_dict(self):
        return dict(
            id=self.id,
            user_id=self.user_id,
            description=self.description,
            scopes=[] if not self.scopes else self.scopes.split(','),
            token=self.token,
            last_used_at=self.last_used_at and self.last_used_at.isoformat(),
        )

    def to_full_dict(self):
        data = self.to_dict()
        data['token'] = self.token
        return data

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def generate_token(cls, user_id):
        data = generate_password_hash(str(user_id))
        method, salt, token = data.split('$')
        return dict(
            token=token,
            salt=salt
        )

    def reset_token(self):
        data = self.generate_token(self.id)
        self.token = data['token']
        self.salt = data['salt']
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, description, scopes):
        self.description = description
        self.scopes = ','.join(scopes)
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def add(cls, user_id, description, scopes=[]):
        token_data = cls.generate_token(user_id)
        obj = cls(
            user_id=user_id,
            description=description,
            scopes=','.join(scopes),
            salt=token_data['salt'],
            token=token_data['token'],
        )
        db.session.add(obj)
        db.session.commit()
        return obj

    def use(self):
        self.last_used_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
