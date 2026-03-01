from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ReceiptItem(BaseModel):
    name: str = Field(..., description="Name of individual item")
    quantity: float = Field(default=1.0)
    price: float = Field(..., description="Price of individual item")

class ReceiptSchema(BaseModel):
    store_name: str = Field(..., description="Name of the store")
    date: Optional[str] = Field(None, description="Date of transaction")
    items: List[ReceiptItem] = Field(..., description="List of purchased items")
    tax: float = Field(default=0.0)
    total: float = Field(..., description="Final amount paid")

class ReceiptResponse(BaseModel):
    status: str
    data: ReceiptSchema
