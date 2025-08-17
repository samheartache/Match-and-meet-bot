from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_columnn


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_columnn(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_columnn(BigInteger)
    username: Mapped[str] = mapped_columnn(String(20))
    age: Mapped[int]
    city: Mapped[str] = mapped_columnn(String(25))
    description: Mapped[str] = mapped_columnn(String(500))
    sex: Mapped[bool]
    search_desire: Mapped[bool | None]
    photo: Mapped[str] = mapped_columnn(String(500))


class Like(Base):
    __tablename__ = 'like'

    id: Mapped[int] = mapped_columnn(primary_key=True, auroincrement=True)
    tg_id: Mapped[int] = mapped_columnn(ForeignKey('user.tg_id', ondelete='CASCADE'))
    liked_id: Mapped[int] = mapped_columnn(ForeignKey('user.tg_id', ondelete='CASCADE'))
    message: Mapped[str] = mapped_columnn(String(100))
    is_answered: Mapped[bool]