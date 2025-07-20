from fastapi import FastAPI, HTTPException, Query, Path, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import uvicorn
from db_manager import DatabaseManager
from schemas import (
    ProductCreateSchema, ProductResponseSchema, 
    OrderCreateSchema, OrderResponseSchema
)
from bson import ObjectId
import re
from datetime import datetime
import os

# Initialize FastAPI application
application = FastAPI(
    title="E-Commerce API System",
    description="Complete e-commerce backend solution with product and order management",
    version="2.0.0",
    docs_url="/api-docs",
    redoc_url="/api-documentation"
)

# Configure CORS
application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Database manager instance
db_manager = DatabaseManager()

@application.on_event("startup")
async def initialize_application():
    """Setup database connection when application starts"""
    await db_manager.initialize_connection()
    print("🚀 E-Commerce API System is ready!")

@application.on_event("shutdown")
async def cleanup_application():
    """Cleanup resources when application shuts down"""
    await db_manager.terminate_connection()
    print("👋 Application shutdown complete")

@application.get("/health")
async def health_check():
    """API health status endpoint"""
    return {
        "service": "E-Commerce Backend API",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }

@application.post("/products", response_model=ProductResponseSchema, status_code=status.HTTP_201_CREATED)
async def add_new_product(product_data: ProductCreateSchema):
    """
    Add a new product to the inventory
    
    Creates a new product with the provided details and returns the created product information.
    """
    try:
        # Prepare product document
        product_document = product_data.dict()
        product_document["creation_timestamp"] = datetime.utcnow()
        product_document["modification_timestamp"] = datetime.utcnow()
        
        # Save to database
        insert_result = await db_manager.product_collection.insert_one(product_document)
        
        # Retrieve the newly created product
        new_product = await db_manager.product_collection.find_one(
            {"_id": insert_result.inserted_id}
        )
        
        # Format response
        new_product["id"] = str(new_product["_id"])
        del new_product["_id"]
        
        return ProductResponseSchema(**new_product)
    
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create product: {str(error)}"
        )

@application.get("/products", response_model=List[ProductResponseSchema])
async def fetch_products_list(
    name: Optional[str] = Query(None, description="Search products by name (case-insensitive)"),
    size: Optional[str] = Query(None, description="Filter products by available size"),
    limit: Optional[int] = Query(10, ge=1, le=50, description="Maximum products to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of products to skip")
):
    """
    Retrieve products with optional filtering and pagination
    
    Supports searching by name, filtering by size, and pagination controls.
    """
    try:
        # Build search criteria
        search_criteria = {}
        
        if name:
            # Case-insensitive name search using regex
            search_criteria["name"] = {
                "$regex": re.escape(name), 
                "$options": "i"
            }
        
        if size:
            # Filter by available sizes
            search_criteria["sizes"] = {"$elemMatch": {"$eq": size}}
        
        # Execute database query with pagination
        products_cursor = (
            db_manager.product_collection
            .find(search_criteria)
            .skip(offset)
            .limit(limit)
            .sort("_id", 1)
        )
        
        products_list = await products_cursor.to_list(length=limit)
        
        # Convert ObjectId to string for JSON serialization
        for product in products_list:
            product["id"] = str(product["_id"])
            del product["_id"]
        
        return [ProductResponseSchema(**product) for product in products_list]
    
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve products: {str(error)}"
        )

@application.post("/orders", response_model=OrderResponseSchema, status_code=status.HTTP_201_CREATED)
async def place_new_order(order_data: OrderCreateSchema):
    """
    Create a new customer order
    
    Validates product availability, checks inventory, and creates the order.
    """
    try:
        # Validate products and inventory
        for order_item in order_data.items:
            product_doc = await db_manager.product_collection.find_one(
                {"_id": ObjectId(order_item.product_id)}
            )
            
            if not product_doc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with ID {order_item.product_id} does not exist"
                )
            
            if product_doc["inventory_count"] < order_item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for {product_doc['name']}. "
                           f"Available: {product_doc['inventory_count']}, "
                           f"Requested: {order_item.quantity}"
                )
        
        # Create order document
        order_document = order_data.dict()
        order_document["order_status"] = "confirmed"
        order_document["creation_timestamp"] = datetime.utcnow()
        order_document["modification_timestamp"] = datetime.utcnow()
        
        # Insert order into database
        order_result = await db_manager.order_collection.insert_one(order_document)
        
        # Update product inventory
        for order_item in order_data.items:
            await db_manager.product_collection.update_one(
                {"_id": ObjectId(order_item.product_id)},
                {"$inc": {"inventory_count": -order_item.quantity}}
            )
        
        # Fetch created order
        created_order = await db_manager.order_collection.find_one(
            {"_id": order_result.inserted_id}
        )
        created_order["id"] = str(created_order["_id"])
        del created_order["_id"]
        
        return OrderResponseSchema(**created_order)
    
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create order: {str(error)}"
        )

@application.get("/orders/{user_id}", response_model=List[OrderResponseSchema])
async def get_customer_orders(
    user_id: str = Path(..., description="Customer user ID"),
    limit: Optional[int] = Query(10, ge=1, le=50, description="Maximum orders to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of orders to skip")
):
    """
    Retrieve all orders for a specific customer
    
    Returns paginated list of orders for the given user ID.
    """
    try:
        # Query orders for specific user
        orders_cursor = (
            db_manager.order_collection
            .find({"user_id": user_id})
            .skip(offset)
            .limit(limit)
            .sort("_id", 1)
        )
        
        orders_list = await orders_cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for order in orders_list:
            order["id"] = str(order["_id"])
            del order["_id"]
        
        return [OrderResponseSchema(**order) for order in orders_list]
    
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve orders: {str(error)}"
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:application", host="0.0.0.0", port=port, reload=True)
