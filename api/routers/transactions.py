


from uuid import UUID
from fastapi import APIRouter

from database.database import DataBase
from database.models.transaction import Transaction
from models.users import TransactionResponse
from services.admin.service import AdminService
from utils.constants import TransactionStatus


class Transactions():
    def __init__(self,db: DataBase, adminservice : AdminService):
        self.router = APIRouter(prefix = "/transactions",tags = ["transactions"])
        self.db = db
        self.adminservice = adminservice

        self.router.add_api_route(path = "/{uuid}",endpoint=self.get_transaction,methods = ["get"])
        self.router.add_api_route(path = "/success/{uuid}",endpoint=self.success_transactoin,methods = ["post"])
        self.router.add_api_route(path = "/cancel/{uuid}",endpoint=self.cancel_transaction,methods = ["post"])

    async def get_transaction(self, uuid: str ) -> TransactionResponse | None:
        async with self.db.session() as s:
            transaction = await Transaction.get_by_id(s,uuid)

        if not transaction:
            return None
        
        await self.adminservice.get_transaction(transaction)

        return TransactionResponse(
            tg_id = transaction.tg_id,
            payment_id = UUID(transaction.payment_id),
            days = transaction.days,
            created_at = transaction.created_at,
            updated_at = transaction.updated_at,
            status = transaction.status
        )
    
    async def success_transactoin(self, uuid: str) -> bool:
        async with self.db.session() as s:
            transaction = await Transaction.get_by_id(s,uuid)

            if not transaction:
                return False

            transaction = await Transaction.update(s,uuid, status = TransactionStatus.COMPLETED)

        await self.adminservice.success_transaction(transaction)
        return True


    async def cancel_transaction(self,uuid: str) -> bool:
        async with self.db.session() as s:
            transaction = await Transaction.get_by_id(s,uuid)

            if not transaction:
                return False
            
            transaction = await Transaction.update(s,uuid, status = TransactionStatus.CANCELED)

        await self.adminservice.cancel_transaction(transaction)
        return True




       
