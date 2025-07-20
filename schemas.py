from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class ProductCreateSchema(BaseModel):
    """Schema for creating new products"""
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    description: Optional[str] = Field(None, max_length=1000, description="Product description")
    category: Optional[str] = Field(None, max_length=100, description="Product category")
    inventory_count: int = Field(..., ge=0, description="Available inventory")
    sizes: Optional[List[str]] = Field(default_factory=list, description="Available sizes")

    @field_validator('name')
    @classmethod
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError('Product name cannot be empty')
        return value.strip()

    @field_validator('sizes')
    @classmethod
    def validate_sizes(cls, value):
        if value:
            # Remove duplicates and empty strings
            return list(set(size.strip().lower() for size in value if size.strip()))
        return []

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Premium Cotton Shirt",
                "price": 45.99,
                "description": "High-quality cotton shirt with modern fit",
                "category": "Apparel",
                "inventory_count": 150,
                "sizes": ["small", "medium", "large", "xl"]
            }
        }
    }

class ProductResponseSchema(BaseModel):
    """Schema for product API responses"""
    id: str = Field(..., description="Unique product identifier", alias="_id")
    name: str
    price: float
    description: Optional[str] = None
    category: Optional[str] = None
    inventory_count: int
    sizes: Optional[List[str]] = []
    creation_timestamp: datetime
    modification_timestamp: datetime

    model_config = {
        "populate_by_name": True
    }

class OrderItemSchema(BaseModel):
    """Schema for individual order items"""
    product_id: str = Field(..., description="Product identifier")
    quantity: int = Field(..., gt=0, description="Item quantity")
    price: float = Field(..., gt=0, description="Unit price")

    @field_validator('product_id')
    @classmethod
    def validate_product_id(cls, value):
        # Basic ObjectId format validation
        if len(value) != 24:
            raise ValueError('Invalid product ID format')
        return value

    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": "507f1f77bcf86cd799439011",
                "quantity": 3,
                "price": 45.99
            }
        }
    }

class OrderCreateSchema(BaseModel):
    """Schema for creating new orders"""
    user_id: str = Field(..., min_length=1, description="Customer user ID")
    items: List[OrderItemSchema] = Field(..., min_length=1, description="Order items")
    total_amount: float = Field(..., gt=0, description="Total order value")

    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, value):
        if not value.strip():
            raise ValueError('User ID cannot be empty')
        return value.strip()

    @field_validator('total_amount')
    @classmethod
    def validate_total_amount(cls, value, info):
        if 'items' in info.data:
            calculated_total = sum(item.quantity * item.price for item in info.data['items'])
            if abs(value - calculated_total) > 0.01:  # Allow small floating point differences
                raise ValueError('Total amount does not match sum of item prices')
        return value

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": "customer_123",
                "items": [
                    {
                        "product_id": "507f1f77bcf86cd799439011",
                        "quantity": 2,
                        "price": 45.99
                    }
                ],
                "total_amount": 91.98
            }
        }
    }

class OrderResponseSchema(BaseModel):
    """Schema for order API responses"""
    id: str = Field(..., description="Unique order identifier", alias="_id")
    user_id: str
    items: List[OrderItemSchema]
    total_amount: float
    order_status: str
    creation_timestamp: datetime
    modification_timestamp: datetime

    model_config = {
        "populate_by_name": True
    }
