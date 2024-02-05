import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from . import Base


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255))
    description = Column(String(255))
    price = Column(String(255))
    submenu_id = Column(
        UUID(as_uuid=True), ForeignKey('submenus.id', ondelete='CASCADE')
    )

    submenu = relationship('Submenu', back_populates='dishes')
