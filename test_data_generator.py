"""
Generate sample data for testing the e-commerce API
"""

import asyncio
import sys
import os
from datetime import datetime
from db_manager import DatabaseManager

async def generate_sample_products():
    """Create sample products for testing"""
    db = DatabaseManager()
    await db.initialize_connection()
    
    sample_products = [
        {
            "name": "Premium Cotton T-Shirt",
            "price": 34.99,
            "description": "Ultra-soft premium cotton t-shirt with modern cut",
            "category": "Clothing",
            "inventory_count": 120,
            "sizes": ["xs", "small", "medium", "large", "xl"],
            "creation_timestamp": datetime.utcnow(),
            "modification_timestamp": datetime.utcnow()
        },
        {
            "name": "Classic Blue Jeans",
            "price": 89.99,
            "description": "Timeless blue jeans with comfortable stretch fabric",
            "category": "Clothing",
            "inventory_count": 80,
            "sizes": ["small", "medium", "large", "xl"],
            "creation_timestamp": datetime.utcnow(),
            "modification_timestamp": datetime.utcnow()
        },
        {
            "name": "Athletic Running Sneakers",
            "price": 149.99,
            "description": "High-performance running shoes with advanced cushioning",
            "category": "Footwear",
            "inventory_count": 60,
            "sizes": ["small", "medium", "large"],
            "creation_timestamp": datetime.utcnow(),
            "modification_timestamp": datetime.utcnow()
        },
        {
            "name": "Bluetooth Wireless Earbuds",
            "price": 179.99,
            "description": "Premium wireless earbuds with active noise cancellation",
            "category": "Electronics",
            "inventory_count": 45,
            "sizes": [],
            "creation_timestamp": datetime.utcnow(),
            "modification_timestamp": datetime.utcnow()
        },
        {
            "name": "Professional Laptop Bag",
            "price": 69.99,
            "description": "Stylish and functional laptop bag for professionals",
            "category": "Accessories",
            "inventory_count": 35,
            "sizes": ["medium", "large"],
            "creation_timestamp": datetime.utcnow(),
            "modification_timestamp": datetime.utcnow()
        },
        {
            "name": "Stainless Steel Water Bottle",
            "price": 24.99,
            "description": "Insulated stainless steel water bottle keeps drinks cold/hot",
            "category": "Accessories",
            "inventory_count": 200,
            "sizes": ["small", "large"],
            "creation_timestamp": datetime.utcnow(),
            "modification_timestamp": datetime.utcnow()
        }
    ]
    
    try:
        # Remove existing test data
        await db.product_collection.delete_many({})
        await db.order_collection.delete_many({})
        print("🧹 Cleared existing test data")
        
        # Insert sample products
        result = await db.product_collection.insert_many(sample_products)
        print(f"✅ Created {len(result.inserted_ids)} sample products")
        
        # Display created products
        products = await db.product_collection.find({}).to_list(length=None)
        print("\n📦 Sample Products Created:")
        for product in products:
            print(f"   • {product['name']} - ${product['price']} ({product['inventory_count']} in stock)")
            
    except Exception as error:
        print(f"❌ Error generating sample data: {error}")
    
    finally:
        await db.terminate_connection()

if __name__ == "__main__":
    print("🚀 Generating sample data for E-Commerce API...")
    asyncio.run(generate_sample_products())
