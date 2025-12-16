from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from uuid import UUID
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from app.models.transaction import Transaction, TransactionType
from app.repositories.base import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    """Repository for Transaction operations."""
    
    def __init__(self, db: Session):
        super().__init__(Transaction, db)
    
    def get_by_user(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_amount: Optional[Decimal] = None,
        max_amount: Optional[Decimal] = None
    ) -> tuple[List[Transaction], int]:
        """Get user transactions with filters and pagination."""
        # Convert string to UUID if necessary
        user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
        
        query = self.db.query(Transaction).filter(Transaction.user_id == user_uuid)
        
        if type:
            query = query.filter(Transaction.type == type)
        if start_date:
            query = query.filter(Transaction.timestamp >= start_date)
        if end_date:
            query = query.filter(Transaction.timestamp <= end_date)
        if min_amount:
            query = query.filter(Transaction.amount >= min_amount)
        if max_amount:
            query = query.filter(Transaction.amount <= max_amount)
        
        total = query.count()
        transactions = query.order_by(Transaction.timestamp.desc()).offset(skip).limit(limit).all()
        
        return transactions, total
    
    def get_user_transaction(self, transaction_id: str, user_id: str) -> Optional[Transaction]:
        """Get a specific transaction for a user."""
        # Convert strings to UUID
        transaction_uuid = UUID(transaction_id) if isinstance(transaction_id, str) else transaction_id
        user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
        
        return self.db.query(Transaction).filter(
            and_(
                Transaction.id == transaction_uuid,
                Transaction.user_id == user_uuid
            )
        ).first()
    
    def get_user_summary(self, user_id: str) -> dict:
        """Get financial summary for a user."""
        # Convert string to UUID
        user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
        
        result = self.db.query(
            func.coalesce(func.sum(func.case((Transaction.type == TransactionType.CREDIT, Transaction.amount), else_=0)), 0).label("total_credits"),
            func.coalesce(func.sum(func.case((Transaction.type == TransactionType.DEBIT, Transaction.amount), else_=0)), 0).label("total_debits"),
            func.count(Transaction.id).label("transaction_count"),
            func.coalesce(func.avg(Transaction.amount), 0).label("avg_transaction")
        ).filter(Transaction.user_id == user_uuid).first()
        
        total_credits = Decimal(str(result.total_credits))
        total_debits = Decimal(str(result.total_debits))
        current_balance = total_credits - total_debits
        transaction_count = result.transaction_count
        avg_transaction = Decimal(str(result.avg_transaction)).quantize(Decimal('0.01'))
        
        return {
            "total_credits": total_credits,
            "total_debits": total_debits,
            "current_balance": current_balance,
            "transaction_count": transaction_count,
            "avg_transaction": avg_transaction
        }