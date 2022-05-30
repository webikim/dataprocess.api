from sqlalchemy import Column, Integer, String, Boolean

from dpapi.db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)

    full_name = Column(String(255))
    email = Column(String(100))
    hashed_password = Column(String(1024))
    disabled = Column(Boolean, default=False)

    def __repr__(self):
        return f'<User: id={self.id}, full_name={self.full_name}, email={self.email}, hashed_password={self.hashed_password} disabled={self.disabled}>'
