from typing import List, Optional
from datetime import datetime

from .base import BaseRepository
from models.users import User, UserIn
from db.users import users
from core.security import hash_pass, verify_pass


class UserRepository(BaseRepository):
    
    # Достаем все
    async def get_all(self, limit: int=100, skip: int=0) -> List[User]:
        query = users.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query)
    
    # Достаем по id
    async def get_by_id(self, id: int) -> Optional[User]:
        query = users.select().where(users.c.id==id)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)
    
    # Достаем по username
    async def get_by_username(self, username: str) -> User:
        query = users.select().where(users.c.username==username)
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)
    
    # Создаем
    async def create(self, u: UserIn) -> User:
        user = User(
            username=u.username,
            password_hash=hash_pass(u.password),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        values = {**user.dict()}
        values.pop("id", None)
        query = users.insert().values(**values)
        user.id = await self.database.execute(query)
        return user
    
    # Обновляем
    async def update(self, id: int, u: UserIn) -> User:
        user = User(
            id=id,
            username=u.username,
            password_hash=hash_pass(u.password),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        values = {**user.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        query = users.update().where(users.c.id==id).values(**values)
        await self.database.execute(query)
        return user
    
    # Удаляем данные
    async def delete(self, id: int) -> bool:
        try:
            query = users.delete().where(users.c.id==id)
            await self.database.execute(query=query)
            return True
        except:
            return False
    
    # Проверка авторизации
    async def check_auth(self, cred) -> bool:
        check_user = await self.get_by_username(cred.username)
        if check_user is None:
            return False
        else:
            if verify_pass(cred.password, check_user.password_hash):
                return True
            else:
                return False
        