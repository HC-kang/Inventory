from sqlalchemy import Integer, String, Column, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.enums.user_approve_status_flag import UserApproveStatusFlag


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=True)
    hashed_password = Column(String(256), nullable=False)
    email = Column(String(256), index=True, nullable=False)
    phone = Column(String(256), nullable=True)
    level = Column(Integer, default=1, nullable=False)
    point = Column(Integer, nullable=False, default=0)
    business_class = Column(String(256), nullable=True)
    business_name = Column(String(256), nullable=True)
    business_president = Column(String(256), nullable=True)
    is_notification = Column(Boolean, default=False)
    approve_status_flag = Column(
        Enum(UserApproveStatusFlag), default=UserApproveStatusFlag.W
    )
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())
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
