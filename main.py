from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import uvicorn
from database import Database
from models import Product, ProductCreate, ProductResponse, Order, OrderCreate, OrderResponse
from bson import ObjectId
import re
from datetime import datetime

app = FastAPI(
    title="HROne E-commerce Backend",
    description="Backend API for e-commerce application built with FastAPI and MongoDB",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = Database()

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    await db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await db.close()

@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {"message": "HROne E-commerce Backend API", "status": "running"}

@app.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate):
    """
    Create a new product
    
    - **name**: Product name (required)
    - **price**: Product price (required)
    - **description**: Product description (optional)
    - **category**: Product category (optional)
    - **inventory_count**: Available inventory (required)
    - **sizes**: Available sizes (optional)
    """
    try:
        # Convert to dict and add timestamp
        product_dict = product.dict()
        product_dict["created_at"] = datetime.utcnow()
        product_dict["updated_at"] = datetime.utcnow()
        
        # Insert into database
        result = await db.products.insert_one(product_dict)
        
        # Fetch the created product
        created_product = await db.products.find_one({"_id": result.inserted_id})
        
        # Convert ObjectId to string for response
        created_product["_id"] = str(created_product["_id"])
        
        return ProductResponse(**created_product)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

@app.get("/products", response_model=List[ProductResponse])
async def list_products(
    name: Optional[str] = Query(None, description="Filter by product name (supports partial search)"),
    size: Optional[str] = Query(None, description="Filter by available size"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of products to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of products to skip")
):
    """
    List products with optional filtering and pagination
    
    - **name**: Filter by product name (partial search supported)
    - **size**: Filter products that have this size available
    - **limit**: Maximum number of products to return (1-100)
    - **offset**: Number of products to skip for pagination
    """
    try:
        # Build filter query
        filter_query = {}
        
        if name:
            # Case-insensitive partial search
            filter_query["name"] = {"$regex": re.escape(name), "$options": "i"}
        
        if size:
            # Filter products that have the specified size
            filter_query["sizes"] = {"$in": [size]}
        
        # Execute query with pagination
        cursor = db.products.find(filter_query).skip(offset).limit(limit).sort("_id", 1)
        products = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string for each product
        for product in products:
            product["_id"] = str(product["_id"])
        
        return [ProductResponse(**product) for product in products]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")

@app.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate):
    """
    Create a new order
    
    - **user_id**: ID of the user placing the order (required)
    - **items**: List of items in the order (required)
    - **total_amount**: Total amount of the order (required)
    """
    try:
        # Validate that all products exist and have sufficient inventory
        for item in order.items:
            product = await db.products.find_one({"_id": ObjectId(item.product_id)})
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            
            if product["inventory_count"] < item.quantity:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Insufficient inventory for product {product['name']}. Available: {product['inventory_count']}, Requested: {item.quantity}"
                )
        
        # Convert to dict and add metadata
        order_dict = order.dict()
        order_dict["status"] = "pending"
        order_dict["created_at"] = datetime.utcnow()
        order_dict["updated_at"] = datetime.utcnow()
        
        # Insert order
        result = await db.orders.insert_one(order_dict)
        
        # Update product inventory
        for item in order.items:
            await db.products.update_one(
                {"_id": ObjectId(item.product_id)},
                {"$inc": {"inventory_count": -item.quantity}}
            )
        
        # Fetch the created order
        created_order = await db.orders.find_one({"_id": result.inserted_id})
        created_order["_id"] = str(created_order["_id"])
        
        return OrderResponse(**created_order)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

@app.get("/orders/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(
    user_id: str = Path(..., description="User ID to fetch orders for"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Number of orders to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of orders to skip")
):
    """
    Get list of orders for a specific user
    
    - **user_id**: ID of the user (path parameter)
    - **limit**: Maximum number of orders to return (1-100)
    - **offset**: Number of orders to skip for pagination
    """
    try:
        # Query orders for the specific user
        cursor = db.orders.find({"user_id": user_id}).skip(offset).limit(limit).sort("_id", 1)
        orders = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string for each order
        for order in orders:
            order["_id"] = str(order["_id"])
        
        return [OrderResponse(**order) for order in orders]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
