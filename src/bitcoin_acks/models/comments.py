from sqlalchemy import (
    Column,
    DateTime,
    String, Enum, func)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import synonym, relationship

from bitcoin_acks.constants import ReviewDecision
from bitcoin_acks.database.base import Base
from bitcoin_acks.models.users import Users


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(String, primary_key=True)

    body = Column(String)

    published_at = Column(DateTime, nullable=False)
    publishedAt = synonym('published_at')

    url = Column(String, nullable=False)

    pull_request_id = Column(String, nullable=False)
    author_id = Column(String)

    auto_detected_ack = Column(Enum(ReviewDecision))
    corrected_ack = Column(Enum(ReviewDecision))

    @hybrid_property
    def ack(self):
        return self.corrected_ack if self.corrected_ack else self.auto_detected_ack

    @ack.expression
    def ack(cls):
        return func.coalesce(cls.auto_detected_ack, cls.corrected_ack)

    author = relationship(Users,
                          primaryjoin=author_id == Users.id,
                          foreign_keys='[Comments.author_id]',
                          backref='comments'
                          )
