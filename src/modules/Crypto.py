from typing import Union, List, Any, ClassVar, Tuple
from abc import ABC, abstractmethod
from random import choice
from hashlib import md5, sha512, blake2b

class Hasher(ABC):
    _IDS: ClassVar[List[str]]= ['1sk', '7wpkgh', 'q0pzth']
    
    @classmethod
    def create_random_hash(cls, data: str) -> str:
        return choice(cls.__subclasses__())().encrypt(data)
        
    @classmethod
    def identify_hash_type(cls, key: str) -> Union['_Md5', '_Sha512', '_Blake2']:
        detect_type: Tuple[bool] = tuple(
            map(lambda id: key.find(id) != -1, Hasher._IDS)
        )
        match detect_type:
            case (True, _, _): return _Md5()
            case (_, True, _): return _Sha512()
            case (_, _, True): return _Blake2()

    @abstractmethod
    def encrypt(self, data: str) -> str:
        pass

class _Md5(Hasher):
    def encrypt(self, data: str) -> str:
        return f'{md5(data.encode()).hexdigest()}{self._IDS[0]}'

class _Sha512(Hasher):
    def encrypt(self, data: str) -> str:
        return f'{sha512(data.encode()).hexdigest()}{self._IDS[1]}'

class _Blake2(Hasher):
    def encrypt(self, data: str) -> str:
        return f'{blake2b(data.encode()).hexdigest()}{self._IDS[2]}'


class PassCrypt:
    pass
