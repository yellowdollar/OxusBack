from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class UserModel(Base):
    __tablename__ = 'tb_user'

    id: Mapped[int] = mapped_column(primary_key = True)
    login: Mapped[str] = mapped_column(nullable = False)
    password: Mapped[str] = mapped_column(nullable = False)