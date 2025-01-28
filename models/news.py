from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class NewsModel(Base):
    __tablename__ = 'tb_news'

    id: Mapped[int] = mapped_column(primary_key = True)
    title: Mapped[str] = mapped_column(nullable = False)
    text: Mapped[str] = mapped_column(nullable = False)
    date: Mapped[str] = mapped_column(nullable = False)
    photo_id: Mapped[int] = mapped_column(ForeignKey('tb_photo.id'), nullable = True)
