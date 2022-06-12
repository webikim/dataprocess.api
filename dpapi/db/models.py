from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey

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


class Script(Base):
    __tablename__ = 'script'
    id = Column(Integer, primary_key=True)

    name = Column(String(100))
    script_type = Column(String(20))
    content = Column(Text)
    note = Column(Text)
    created = Column(DateTime)
    updated = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return f"<Script id={self.id}, name={self.name}, script_type={self.script_type}, content={len(self.content)}," \
               f"note{self.note}, created={self.created}, user_id={self.user_id}>"


class RunLog(Base):
    __tablename__ = 'run_log'
    id = Column(Integer, primary_key=True)

    in_from_id =Column(Integer)
    requested = Column(DateTime)
    started = Column(DateTime)
    finished = Column(DateTime)
    status = Column(String(20))
    script_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return f"<RunLog id={self.id}, requested={self.requested}, started={self.started}, finished={self.finished}," \
               f"status={self.status}, script_id={self.script_id}, user_id={self.user_id}>"
