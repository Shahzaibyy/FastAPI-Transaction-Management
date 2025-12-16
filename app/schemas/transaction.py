# FILE: app/schemas/transaction.py
# ============================================================================
from datetime import datetime
from decimal import Decimal
from typing import Optional, Literal, Any
from uuid import UUID
from pydantic import BaseModel, Field, field_validator, ConfigDict


class TransactionBase(BaseModel):
    """Base transaction schema."""
    amount: Decimal = Field(..., gt=0, decimal_places=2, max_digits=10)
    type: Literal["credit", "debit"]
    description: str = Field(..., max_length=500, min_length=1)
    timestamp: datetime


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        """Ensure amount is positive."""
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction."""
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2, max_digits=10)
    type: Optional[Literal["credit", "debit"]] = None
    description: Optional[str] = Field(None, max_length=500, min_length=1)
    timestamp: Optional[datetime] = None


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
    id: UUID
    user_id: UUID
    created_at: datetime 
    
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )
    
    @field_validator('type', mode='before')
    @classmethod
    def convert_enum_to_string(cls, v: Any) -> str:
        """Convert TransactionType enum to string value."""
        if hasattr(v, 'value'):
            return v.value
        return v


class TransactionListResponse(BaseModel):
    """Schema for paginated transaction list."""
    items: list[TransactionResponse]
    total: int
    page: int
    size: int
    pages: int


class TransactionSummary(BaseModel):
    """Schema for transaction summary/analytics."""
    total_credits: Decimal
    total_debits: Decimal
    current_balance: Decimal
    transaction_count: int
    avg_transaction: Decimal