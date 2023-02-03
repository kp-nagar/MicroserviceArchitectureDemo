import os
import time
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker


# https://docs.sqlalchemy.org/en/14/faq/connections.html#faq-execute-retry
def reconnecting_engine(engine, num_retries, retry_interval):
    def _run_with_retries(fn, context, cursor, statement, *arg, **kw):
        for retry in range(num_retries + 1):
            try:
                fn(cursor, statement, context=context, *arg)
            except engine.dialect.dbapi.Error as raw_dbapi_err:
                connection = context.root_connection
                if engine.dialect.is_disconnect(
                        raw_dbapi_err, connection, cursor
                ):
                    if retry > num_retries:
                        raise
                    engine.logger.error(
                        "disconnection error, retrying operation",
                        exc_info=True,
                    )
                    connection.invalidate()

                    # use SQLAlchemy 2.0 API if available
                    if hasattr(connection, "rollback"):
                        connection.rollback()
                    else:
                        trans = connection.get_transaction()
                        if trans:
                            trans.rollback()

                    time.sleep(retry_interval)
                    context.cursor = cursor = connection.connection.cursor()
                else:
                    raise
            else:
                return True

    e = engine.execution_options(isolation_level="READ COMMITTED")

    @event.listens_for(e, "do_execute_no_params")
    def do_execute_no_params(cursor, statement, context):
        return _run_with_retries(
            context.dialect.do_execute_no_params, context, cursor, statement
        )

    @event.listens_for(e, "do_execute")
    def do_execute(cursor, statement, parameters, context):
        return _run_with_retries(
            context.dialect.do_execute, context, cursor, statement, parameters
        )

    return e


SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOSTNAME']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
engine = reconnecting_engine(
    create_engine(SQLALCHEMY_DATABASE_URI,
                  echo_pool=True,
                  pool_pre_ping=True
                  ),
    num_retries=5,
    retry_interval=2,
)

Session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=False))
