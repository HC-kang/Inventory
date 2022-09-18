from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    surname = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    recipes = relationship(
        "Recipe",
        cascade="all,delete-orphan",
        back_populates="submitter",
        uselist=True,
    )
    storages = relationship(
        "Storage",
        cascade="all,delete-orphan",
        back_populates="user",
        uselist=True,
    )

    # New addition
    hashed_password = Column(String(256), nullable=False)
