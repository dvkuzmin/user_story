import dataclasses
import logging
from dataclasses import dataclass, fields

logger = logging.getLogger(__name__)


@dataclass
class RequestData:
    id: int
    delay: int

    @classmethod
    def is_valid(cls, data_dict):
        for field in fields(cls):
            if field.name not in data_dict:
                logger.error(f'Field {field.name} not provided in request')
                raise ValueError(f'Field {field.name} not provided in request')
            if not isinstance(data_dict[field.name], field.type):
                logger.error(f'Invalid type for field {field.name} in request')
                raise ValueError(f'Invalid type for field {field.name}')

        return True
