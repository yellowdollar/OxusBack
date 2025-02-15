from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class ForumModel(Base):
    __tablename__ = 'tb_forum'

    id: Mapped[int] = mapped_column(primary_key = True)
    year: Mapped[str] = mapped_column(nullable = False)
    place: Mapped[str] = mapped_column(nullable = False)
    place_eng: Mapped[str] = mapped_column(nullable = False)