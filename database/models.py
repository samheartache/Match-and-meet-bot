from sqlalchemy import BigInteger, String, ForeignKey, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(20))
    age: Mapped[int]
    city: Mapped[str] = mapped_column(String(25))
    description: Mapped[str | None] = mapped_column(String(500))
    sex: Mapped[bool]
    search_desire: Mapped[bool | None]
    searched_by: Mapped[bool | None]
    photo: Mapped[str] = mapped_column(String(500))
    time_created: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    time_updated: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),\
                                                            onupdate=datetime.datetime.utcnow)


class Like(Base):
    __tablename__ = 'like'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey('user.tg_id', ondelete='CASCADE'))
    liked_id: Mapped[int] = mapped_column(ForeignKey('user.tg_id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship('User', foreign_keys=[tg_id], backref='likes_sent')
    liked_user: Mapped['User'] = relationship('User', foreign_keys=[tg_id], backref='likes_received')

    is_like: Mapped[bool]
    message: Mapped[str | None] = mapped_column(String(100))
    is_watched: Mapped[bool | None]
    is_mutual: Mapped[bool]
    time_created: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))