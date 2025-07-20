"""
Script to seed the database with sample data for testing
Run this script to populate your database with sample products
"""

import asyncio
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Database
from datetime import datetime

async def seed_products():
    """Seed database with sample products"""
    db = Database()
    await db.connect()
    
    sample_products = [
        {
            "name": "Cotton T-Shirt",
            "price": 29.99,
            "description": "Comfortable cotton t-shirt perfect for everyday wear",
            "category": "Clothing",
            "inventory_count": 100,
            "sizes": ["small", "medium", "large", "xl"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Denim Jeans",
            "price": 79.99,
            "description": "Classic blue denim jeans with modern fit",
            "category": "Clothing",
            "inventory_count": 50,
            "sizes": ["small", "medium", "large"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Running Shoes",
            "price": 129.99,
            "description": "Lightweight running shoes for optimal performance",
            "category": "Footwear",
            "inventory_count": 75,
            "sizes": ["small", "medium", "large"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Wireless Headphones",
            "price": 199.99,
            "description": "High-quality wireless headphones with noise cancellation",
            "category": "Electronics",
            "inventory_count": 30,
            "sizes": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Laptop Backpack",
            "price": 59.99,
            "description": "Durable laptop backpack with multiple compartments",
            "category": "Accessories",
            "inventory_count": 40,
            "sizes": ["medium", "large"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    try:
        # Clear existing products (optional)
        await db.products.delete_many({})
        print("Cleared existing products")
        
        # Insert sample products
        result = await db.products.insert_many(sample_products)
        print(f"Inserted {len(result.inserted_ids)} sample products")
        
        # Display inserted products
        products = await db.products.find({}).to_list(length=None)
        print("\nSample products created:")
        for product in products:
            print(f"- {product['name']} (${product['price']}) - {product['inventory_count']} in stock")
            
    except Exception as e:
        print(f"Error seeding data: {e}")
    
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(seed_products())
