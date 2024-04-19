from sqlalchemy import Column, Text, Integer, ForeignKey

from app.models.abstract_model import AbstractModel


class Donation(AbstractModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
