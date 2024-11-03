from typeing import Callable
from neo4j import GraphDatabase as Neo4JGaphDb
from app.core.conncurrency import cpu_bound_task

class AsyncGraphDatabase:
    """Async wrapper over Neo4J driver, since it doesn't natively expose an async interface.
       
       HTTP APIs + https could have been used to avoid the need to run_in_executor
       calls, at the cost of less convenient responses parsing and slightly worse performance.
    """
    
    def __init__(self, uri: str, user: str, password: str):
        self._driver = Neo4JGaphDb.driver(uri, auth=(user, password))
        
    async def write_tx(self, tx_func: Callable):
        """Async wrapper over Neo4J 'write_transaction' method."""
        
        def write_transaction():
            with self._driver.session() as session:
                return session.write_transaction(tx_func)
            
        return await cpu_bound_task(write_transaction)
        
    async def read_tx(self, tx_func: Callable):
        """Async wrapper over Neo4J 'read_transaction' method."""
        
        def read_transaction():
            with self._driver.session() as session:
                return session.read_transaction(tx_func)
        return await cpu_bound_task(read_transaction)
    