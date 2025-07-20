from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ProductCreate(BaseModel):
    """Schema for creating a new product"""
    name: str = Field(..., description="Product name")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    description: Optional[str] = Field(None, description="Product description")
    category: Optional[str] = Field(None, description="Product category")
    inventory_count: int = Field(..., ge=0, description="Available inventory count")
    sizes: Optional[List[str]] = Field(default=[], description="Available sizes")

    class Config:
        schema_extra = {
            "example": {
                "name": "Cotton T-Shirt",
                "price": 29.99,
                "description": "Comfortable cotton t-shirt",
                "category": "Clothing",
                "inventory_count": 100,
                "sizes": ["small", "medium", "large"]
            }
        }

class ProductResponse(BaseModel):
    """Schema for product response"""
    _id: str = Field(..., description="Product ID")
    name: str
    price: float
    description: Optional[str] = None
    category: Optional[str] = None
    inventory_count: int
    sizes: Optional[List[str]] = []
    created_at: datetime
    updated_at: datetime

class OrderItem(BaseModel):
    """Schema for order items"""
    product_id: str = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity (must be positive)")
    price: float = Field(..., gt=0, description="Price per item")

    class Config:
        schema_extra = {
            "example": {
                "product_id": "64a7b8c9d1e2f3a4b5c6d7e8",
                "quantity": 2,
                "price": 29.99
            }
        }

class OrderCreate(BaseModel):
    """Schema for creating a new order"""
    user_id: str = Field(..., description="User ID placing the order")
    items: List[OrderItem] = Field(..., min_items=1, description="List of order items")
    total_amount: float = Field(..., gt=0, description="Total order amount")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "items": [
                    {
                        "product_id": "64a7b8c9d1e2f3a4b5c6d7e8",
                        "quantity": 2,
                        "price": 29.99
                    }
                ],
                "total_amount": 59.98
            }
        }

class OrderResponse(BaseModel):
    """Schema for order response"""
    _id: str = Field(..., description="Order ID")
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime

class Product(BaseModel):
    """Internal product model"""
    name: str
    price: float
    description: Optional[str] = None
    category: Optional[str] = None
    inventory_count: int
    sizes: Optional[List[str]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Order(BaseModel):
    """Internal order model"""
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
