from sqlalchemy.orm.decl_api import DeclarativeMeta
from random import randint
import re
import string
import hashlib
import os

string.ascii_letters

class Utils:
    RE_EMAIL = r'\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b'
    RE_URL   = r'https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(:[a-zA-Z0-9]*)?/?([a-zA-Z0-9\-\._\?\,]*)?'

    @staticmethod
    def generate_token(_string: str):
        return hashlib.sha256(
            (_string+Utils.__randomstring()).encode()
        ).hexdigest()

    @staticmethod
    def __randomstring():
        return ''.join([
            string.ascii_letters[
                randint(0, len(string.ascii_letters)-1)
            ] 
            for _ in range(30)
        ])
    
    @staticmethod
    def serializer(
        instance: DeclarativeMeta | list[DeclarativeMeta],
        attrs: dict[str]
    ):
        if not isinstance(instance, list):
            if not attrs or instance is None:
                return instance
            
            return {
                attr: Utils.serializer(getattr(instance, attr), attrs[attr]) for attr in attrs
            }
        
        return [
            Utils.serializer(_instance, attrs) for _instance in instance
        ]
    
    @staticmethod
    def validate(data: dict, protocols: dict[str, dict]):
        msg   = {}

        for attr, protocol in protocols.items():
            if protocol.get('required') and not attr in data:
                msg[attr] = 'This attr is required'
            
            if attr in data:
                if protocol.get('type') and not isinstance(data[attr], protocol['type']):
                    msg[attr] = f'This attr must be a {protocol["type"]} and not a {type(data[attr])}'
                elif protocol.get('max-length') and len(data[attr]) > protocol["max-length"]:
                    msg[attr] = f'This attr must have a length less {protocol["max-length"]+1}'
                elif protocol.get('min-length') and len(data[attr]) < protocol["min-length"]:
                    msg[attr] = f'This attr must have a length greater {protocol["min-length"]-1}'
                elif protocol.get('length') and not len(data[attr]) == protocol["length"]:
                    msg[attr] = f'This attr must have a length eqaul {protocol["length"]}'
                elif protocol.get('values') and data[attr] not in protocol['values']:
                    msg[attr] = f'This attr must be in {protocol["values"]}'
                elif protocol.get('re') and not re.fullmatch(re.compile(protocol['re']), data[attr]):
                    msg[attr] = f'This attr must be compatibly with re {protocol["re"]}'

        if not msg == {}:
            return False, msg

        return True, None

    @staticmethod
    def up_env():
        if os.path.exists('./.env'):
            with open('./.env') as file:
                for line in file.readlines():
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

class Env():
    def __getattribute__(self, name: str):
        return os.getenv(name)