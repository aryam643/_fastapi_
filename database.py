import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class Database:
    """Database connection and operations handler"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database = None
        self.products = None
        self.orders = None
        
        # MongoDB connection string - use environment variable or default
        self.connection_string = os.getenv(
            "MONGODB_URL", 
            "mongodb+srv://username:password@cluster.mongodb.net/hrone_ecommerce?retryWrites=true&w=majority"
        )
        self.database_name = os.getenv("DATABASE_NAME", "hrone_ecommerce")
    
    async def connect(self):
        """Establish database connection"""
        try:
            self.client = AsyncIOMotorClient(self.connection_string)
            self.database = self.client[self.database_name]
            self.products = self.database.products
            self.orders = self.database.orders
            
            # Test the connection
            await self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            
            # Create indexes for better performance
            await self.create_indexes()
            
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise
    
    async def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")
    
    async def create_indexes(self):
        """Create database indexes for better query performance"""
        try:
            # Index for product name search
            await self.products.create_index("name")
            
            # Index for product sizes
            await self.products.create_index("sizes")
            
            # Index for product category
            await self.products.create_index("category")
            
            # Index for orders by user_id
            await self.orders.create_index("user_id")
            
            # Index for order status
            await self.orders.create_index("status")
            
            print("Database indexes created successfully")
            
        except Exception as e:
            print(f"Error creating indexes: {e}")
