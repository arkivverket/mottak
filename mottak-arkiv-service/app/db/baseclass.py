from typing import Any
import re
from sqlalchemy.ext.declarative import as_declarative, declared_attr



@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__
        # This beutiful line transforms CamelCase to snake_case and adds an s
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
