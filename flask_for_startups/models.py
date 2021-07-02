# Standard Library imports

# Core Flask imports
from flask_login import UserMixin

# Third-party imports
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

# App imports
from flask_for_startups import db_manager
from flask_for_startups.utils.sqlalchemy_utils import utcnow

# alias
Base = db_manager.base

class Account(Base):
    __tablename__ = 'accounts'
    account_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    created_at = Column(DateTime, server_default=utcnow())

    users = relationship("User", back_populates="account")

class User(UserMixin, Base):
    __tablename__ = 'users'
    user_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    username = Column(String)
    email = Column(String, unique=True)
    roles = Column(ARRAY(String), nullable=False, server_default="{user}")
    created_at = Column(DateTime, server_default=utcnow())
    account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.account_id'), nullable=False)

    account = relationship("Account", back_populates="users")

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return '<User {}>'.format(self.username)
