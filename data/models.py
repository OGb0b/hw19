from sqlalchemy import (Column, Integer, ForeignKey, VARCHAR)
from sqlalchemy.ext.declarative import declarative_base
import warnings
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:0000@127.0.0.1:5432/postgres")
warnings.filterwarnings('ignore')
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(50), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

class Notes(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    note_text = Column(VARCHAR(1000), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Notes(id={self.id}, note_text={self.note_text}, user_id={self.user_id})>"


if __name__ == '__main__':
    engine = create_engine("postgresql+psycopg2://postgres:0000@127.0.0.1:5432/postgres")
    with engine.connect() as conn:
        Base.metadata.create_all(engine)