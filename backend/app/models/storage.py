from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Storage(Base):
    __tablename__ = "storages"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="storages")
