from music.adapters.repository import AbstractRepository, RepositoryException

class MemoryRepository(AbstractRepository):
    
    def __init__(self):
        self.__users = list()
        self.__tracks = list()
        