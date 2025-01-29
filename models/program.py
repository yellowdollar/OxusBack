from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class ProgramModel(Base):
    __tablename__ = 'tb_program'

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(nullable = False)
    time: Mapped[str] = mapped_column(nullable = False)
    title: Mapped[str] = mapped_column(nullable = False)
    text: Mapped[str] = mapped_column(nullable = False)
    forum_id: Mapped[int] = mapped_column(ForeignKey('tb_forum.id'))