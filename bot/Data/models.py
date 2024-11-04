from re import T
from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BannedWord(Base):
    __tablename__ = 'banned_words'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String, unique=True, nullable=False)


class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    warning_count = Column(Integer, default=0)  # Счетчик предупреждений
    birth_date = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(username={self.username}, first_name={self.first_name}, last_name={self.last_name})>"


class ChislaSoznaniya(Base):
    __tablename__ = 'chisla_soznaniya'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=True)
    
    
class Missions(Base):
    __tablename__ = 'missions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=True)
    
    

class Years(Base):
    __tablename__ = 'years'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=True)