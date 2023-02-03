import abc

from logger.logger import logger


class AbstractUnitOfWork(abc.ABC):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.__del__()

    @abc.abstractmethod
    def safe_commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __del__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        from db.db_session import Session
        self.db_session = Session()

    def safe_commit(self):
        if self.db_session:
            try:
                self.db_session.commit()
            except:
                self.db_session.rollback()
                raise

    def rollback(self):
        if self.db_session:
            try:
                self.db_session.rollback()
            except:
                raise

    def __del__(self):
        if self.db_session:
            from db.db_session import Session
            try:
                self.safe_commit()
            finally:
                Session.remove()
                del self.db_session
                self.db_session = None

    def __enter__(self):
        from db.db_session import Session
        logger.info('Starting')
        if self.db_session:
            self.__del__()
        self.db_session = Session()
        return self

    def __exit__(self, *exc):
        logger.info('Finishing')
        if self.db_session:
            self.__del__()
