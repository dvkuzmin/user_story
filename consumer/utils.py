import json
import logging

logger = logging.getLogger(__name__)


def load_data(request: str):
    try:
        request_data = json.loads(request)
        return request_data
    except json.JSONDecodeError:
        logger.exception('Json Decode Error')
