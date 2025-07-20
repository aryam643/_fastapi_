import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import asyncio

class DatabaseManager:
    """Handles all database operations and connections"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database = None
        self.product_collection = None
        self.order_collection = None
        
        # Database configuration
        self.mongo_uri = "mongodb+srv://aryamsharmadev:181006@db.mljp9di.mongodb.net/?retryWrites=true&w=majority&appName=db"
        self.db_name = os.getenv("DATABASE_NAME", "ecommerce_system")
    
    async def initialize_connection(self):
        """Establish connection to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(self.mongo_uri)
            self.database = self.client[self.db_name]
            self.product_collection = self.database.products
            self.order_collection = self.database.orders
            
            # Verify connection
            await self.client.admin.command('ping')
            print("✅ MongoDB connection established successfully")
            
            # Setup database indexes
            await self.setup_database_indexes()
            
        except Exception as error:
            print(f"❌ MongoDB connection failed: {error}")
            raise
    
    async def terminate_connection(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("🔌 MongoDB connection closed")
    
    async def setup_database_indexes(self):
        """Create database indexes for optimal performance"""
        try:
            # Product collection indexes
            await self.product_collection.create_index("name")
            await self.product_collection.create_index("category")
            await self.product_collection.create_index("sizes")
            await self.product_collection.create_index("price")
            
            # Order collection indexes
            await self.order_collection.create_index("user_id")
            await self.order_collection.create_index("order_status")
            await self.order_collection.create_index("creation_timestamp")
            
            # Compound indexes for better query performance
            await self.product_collection.create_index([
                ("category", 1), 
                ("price", 1)
            ])
            
            await self.order_collection.create_index([
                ("user_id", 1), 
                ("creation_timestamp", -1)
            ])
            
            print("📊 Database indexes created successfully")
            
        except Exception as error:
            print(f"⚠️ Error creating indexes: {error}")

    async def get_database_stats(self):
        """Get database statistics for monitoring"""
        try:
            product_count = await self.product_collection.count_documents({})
            order_count = await self.order_collection.count_documents({})
            
            return {
                "products_count": product_count,
                "orders_count": order_count,
                "database_name": self.db_name
            }
        except Exception as error:
            print(f"Error getting database stats: {error}")
            return None
