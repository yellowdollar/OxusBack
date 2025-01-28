from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base


class PhotoModel(Base):
    __tablename__ = 'tb_photo'

    id: Mapped[int] = mapped_column(primary_key = True)
    photo_path: Mapped[str] = mapped_column(nullable = False)