from database.database import async_session
from abc import abstractmethod

from sqlalchemy import insert, select, delete, update


class AbstractRepository:

    @abstractmethod
    async def add():
        return NotImplementedError
    
    @abstractmethod
    async def get():
        return NotImplementedError
    
    @abstractmethod
    async def delete():
        return NotImplementedError
    
    @abstractmethod
    async def update():
        return NotImplementedError
    
class SQLALchemyRepository(AbstractRepository):
    model = None

    async def add(self, data: dict):
        async with async_session() as session:
            stmt = (
                insert(self.model)
                .values(**data)
                .returning(self.model)
            )

            try:
                result = await session.execute(stmt)
                await session.commit()

                return result.scalars().all()
            except Exception as error:
                await session.rollback()
                return {
                    'message': f'Error {str(error)}',
                    'status_code': '400'
                }
    
    async def get(self, filters: dict):
        async with async_session() as session:
            stmt = (
                select(self.model)
                .filter_by(**filters)
            )
            try:
                result = await session.execute(stmt)
                return result.scalars().all()
            except Exception as error:
                await session.rollback()
                return {
                    'message': f'Error {str(error)}',
                    'status_code': '400'
                }
            
    async def delete(self, id):
        async with async_session() as session:
            stmt = (
                delete(self.model)
                .where(self.model.id == id)
                .returning(self.model)
            )

            try:
                result = await session.execute(stmt)
                await session.commit()

                return result.scalars().all()
            except Exception as error:
                await session.rollback()
                return {
                    'message': f'Error: {str(error)}',
                    'status_code': '400'
                }
            
    async def update(self, id: int, data: dict):
        async with async_session() as session:
            stmt = (
                update(self.model)
                .values(**data)
                .where(self.model.id == id)
                .returning(self.model)
            )

            try:
                result = await session.execute(stmt)
                await session.commit()

                return result.scalars().all()
            
            except Exception as error:
                return {
                    'message': f'Error: {str(error)}',
                    'status_code': '400'
                }
