from typing import Optional, List
from ...domain.ports.user_repository import UserRepository
from ...domain.entities.user import User
from ...shared.config import brasilia_now
from .mongo_repository import get_users_collection


class MongoUserRepository(UserRepository):
    """Implementação do repositório de usuários usando MongoDB."""
    
    async def create(self, user: User) -> User:
        """Cria um novo usuário."""
        user_dict = user.dict()
        user_dict["created_at"] = brasilia_now()
        
        result = await get_users_collection().insert_one(user_dict)
        user.id = str(result.inserted_id)
        
        return user
    
    async def find_by_username(self, username: str) -> Optional[User]:
        """Busca usuário por username."""
        user_dict = await get_users_collection().find_one({"username": username})
        if user_dict:
            user_dict["id"] = str(user_dict["_id"])
            return User(**user_dict)
        return None
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email."""
        user_dict = await get_users_collection().find_one({"email": email})
        if user_dict:
            user_dict["id"] = str(user_dict["_id"])
            return User(**user_dict)
        return None
    
    async def find_all(self) -> List[User]:
        """Busca todos os usuários."""
        cursor = get_users_collection().find()
        users = []
        async for user_dict in cursor:
            user_dict["id"] = str(user_dict["_id"])
            users.append(User(**user_dict))
        return users
