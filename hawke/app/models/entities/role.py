from typing import List, Optional

class Role:
    _roles = [
        {"id": 1, "name": "root", "description": "Usuário boladão"},
        {"id": 2, "name": "admin", "description": "Administrador do sistema"},
        {"id": 3, "name": "register", "description": "Usuário comum"},
        {"id": 4, "name": "organizer", "description": "Organizador de eventos"}
    ]

    @classmethod
    def get_all(cls) -> List[dict]:
        return cls._roles

    @classmethod
    def get_by_id(cls, role_id: int) -> Optional[dict]:
        return next((role for role in cls._roles if role["id"] == role_id), None)

    @classmethod
    def get_by_name(cls, name: str) -> Optional[dict]:
        return next((role for role in cls._roles if role["name"] == name), None)