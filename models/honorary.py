from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class HonoraryModel(Base):
    __tablename__ = 'tb_honorary'

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(nullable = False)
    name_eng: Mapped[str] = mapped_column(nullable = False)
    work_place: Mapped[str] = mapped_column(nullable = False)
    work_place_eng: Mapped[str] = mapped_column(nullabele = False)
    forum_id: Mapped[int] = mapped_column(ForeignKey('tb_forum.id'))
    photo_id: Mapped[int] = mapped_column(ForeignKey('tb_photo.id')) 