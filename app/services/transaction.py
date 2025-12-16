from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.repositories.transaction import TransactionRepository
from app.schemas.transaction import (
    TransactionCreate,
    TransactionListResponse,
    TransactionResponse,
    TransactionSummary
)


class TransactionService:
    """Service for transaction operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.transaction_repo = TransactionRepository(db)
    
    def create_transaction(self, user_id: str, transaction_data: TransactionCreate) -> Transaction:
        """Create a new transaction."""
        # Convert string to UUID
        user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
        
        transaction = Transaction(
            user_id=user_uuid,
            amount=transaction_data.amount,
            type=transaction_data.type,
            description=transaction_data.description,
            timestamp=transaction_data.timestamp
        )
        
        return self.transaction_repo.create(transaction)
    
    def get_user_transactions(
        self,
        user_id: str,
        page: int = 1,
        limit: int = 20,
        type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_amount: Optional[Decimal] = None,
        max_amount: Optional[Decimal] = None
    ) -> TransactionListResponse:
        """Get user transactions with filters and pagination."""
        skip = (page - 1) * limit
        
        transactions, total = self.transaction_repo.get_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            type=type,
            start_date=start_date,
            end_date=end_date,
            min_amount=min_amount,
            max_amount=max_amount
        )
        
        pages = (total + limit - 1) // limit
        
        return TransactionListResponse(
            items=[TransactionResponse.model_validate(t) for t in transactions],
            total=total,
            page=page,
            size=limit,
            pages=pages
        )
    
    def get_transaction(self, transaction_id: str, user_id: str) -> Transaction:
        """Get a specific transaction."""
        transaction = self.transaction_repo.get_user_transaction(transaction_id, user_id)
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        return transaction
    
    def delete_transaction(self, transaction_id: str, user_id: str) -> bool:
        """Delete a transaction."""
        transaction = self.transaction_repo.get_user_transaction(transaction_id, user_id)
        
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found"
            )
        
        return self.transaction_repo.delete(transaction_id)
    
    def get_user_summary(self, user_id: str) -> TransactionSummary:
        """Get user financial summary."""
        summary = self.transaction_repo.get_user_summary(user_id)
        return TransactionSummary(**summary)