from typing import List
from ...domain.ports.log_repository import LogRepository
from ...domain.entities.log import Log
from ...shared.config import brasilia_now
from .mongo_repository import get_logs_collection


class MongoLogRepository(LogRepository):
    """Implementação do repositório de logs usando MongoDB."""
    
    async def create(self, log: Log) -> Log:
        """Cria um novo log."""
        log_dict = log.dict()
        log_dict["created_at"] = brasilia_now()
        
        result = await get_logs_collection().insert_one(log_dict)
        log.id = str(result.inserted_id)
        
        return log
    
    async def find_recent(self, limit: int = 100) -> List[Log]:
        """Busca logs recentes."""
        cursor = get_logs_collection().find().sort("timestamp", -1).limit(limit)
        logs = []
        async for log_dict in cursor:
            log_dict["id"] = str(log_dict["_id"])
            logs.append(Log(**log_dict))
        return logs
    
    async def find_all(self) -> List[Log]:
        """Busca todos os logs."""
        cursor = get_logs_collection().find()
        logs = []
        async for log_dict in cursor:
            log_dict["id"] = str(log_dict["_id"])
            logs.append(Log(**log_dict))
        return logs
