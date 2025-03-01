from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class RegistModel(Base):
    __tablename__ = 'tb_regist'

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(nullable = False)
    surname: Mapped[str] = mapped_column(nullable = False)
    email: Mapped[str] = mapped_column(nullable = False)
    phone: Mapped[str] = mapped_column(nullable = False)
    job_title: Mapped[str] = mapped_column(nullable = False)
    smth: Mapped[str] = mapped_column(nullable = False)