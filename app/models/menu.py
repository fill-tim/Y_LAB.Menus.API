import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from . import Base


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255))
    description = Column(String(255))

    submenus = relationship('Submenu', back_populates='menu')
