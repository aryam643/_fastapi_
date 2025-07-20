<<<<<<< HEAD
# _fastapi_
=======
# HROne E-commerce Backend API

A FastAPI-based e-commerce backend application built for the HROne Backend Intern hiring task. This application provides RESTful APIs for managing products and orders with MongoDB as the database.

## 🚀 Features

- **Product Management**: Create and list products with filtering capabilities
- **Order Management**: Create orders and retrieve user order history
- **MongoDB Integration**: Async MongoDB operations using Motor
- **Data Validation**: Comprehensive request/response validation using Pydantic
- **Filtering & Pagination**: Advanced filtering and pagination support
- **Error Handling**: Robust error handling and validation
- **Documentation**: Auto-generated API documentation with Swagger UI
- **Performance**: Optimized database queries with proper indexing

## 📋 API Endpoints

### Products
- `POST /products` - Create a new product
- `GET /products` - List products with optional filtering

### Orders
- `POST /orders` - Create a new order
- `GET /orders/{user_id}` - Get orders for a specific user

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: MongoDB with Motor (async driver)
- **Validation**: Pydantic v2
- **Documentation**: Automatic OpenAPI/Swagger documentation

## 📦 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- MongoDB Atlas account (free M0 cluster)

### Local Development

1. **Clone the repository**
\`\`\`bash
git clone <your-repo-url>
cd hrone-backend-assignment
\`\`\`

2. **Install dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Set up environment variables**
Create a `.env` file in the root directory:
\`\`\`env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/hrone_ecommerce?retryWrites=true&w=majority
DATABASE_NAME=hrone_ecommerce
PORT=8000
\`\`\`

4. **Run the application**
\`\`\`bash
python main.py
\`\`\`

The API will be available at `http://localhost:8000`

### Seed Sample Data (Optional)
\`\`\`bash
python scripts/seed_data.py
\`\`\`

## 📚 API Documentation

Once the application is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔧 API Usage Examples

### Create Product
\`\`\`bash
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cotton T-Shirt",
    "price": 29.99,
    "description": "Comfortable cotton t-shirt",
    "category": "Clothing",
    "inventory_count": 100,
    "sizes": ["small", "medium", "large"]
  }'
\`\`\`

### List Products with Filtering
\`\`\`bash
# Get all products
curl "http://localhost:8000/products"

# Filter by name
curl "http://localhost:8000/products?name=shirt"

# Filter by size
curl "http://localhost:8000/products?size=large"

# With pagination
curl "http://localhost:8000/products?limit=5&offset=10"
\`\`\`

### Create Order
\`\`\`bash
curl -X POST "http://localhost:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "items": [
      {
        "product_id": "64a7b8c9d1e2f3a4b5c6d7e8",
        "quantity": 2,
        "price": 29.99
      }
    ],
    "total_amount": 59.98
  }'
\`\`\`

### Get User Orders
\`\`\`bash
curl "http://localhost:8000/orders/user123?limit=10&offset=0"
\`\`\`

## 🏗️ Project Structure

\`\`\`
hrone-backend-assignment/
├── main.py              # FastAPI application and route handlers
├── models.py            # Pydantic models for request/response validation
├── database.py          # MongoDB connection and operations
├── config.py            # Application configuration
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── README.md           # Project documentation
└── scripts/
    └── seed_data.py    # Database seeding script
\`\`\`

## 🗄️ Database Schema

### Products Collection
\`\`\`json
{
  "_id": "ObjectId",
  "name": "string",
  "price": "number",
  "description": "string (optional)",
  "category": "string (optional)",
  "inventory_count": "number",
  "sizes": ["array of strings"],
  "created_at": "datetime",
  "updated_at": "datetime"
}
\`\`\`

### Orders Collection
\`\`\`json
{
  "_id": "ObjectId",
  "user_id": "string",
  "items": [
    {
      "product_id": "string",
      "quantity": "number",
      "price": "number"
    }
  ],
  "total_amount": "number",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
\`\`\`

## 🚀 Deployment

### Deploy to Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables:
   - `MONGODB_URL`: Your MongoDB Atlas connection string
   - `DATABASE_NAME`: Your database name

### Deploy to Railway

1. Connect your GitHub repository to Railway
2. Railway will auto-detect the Python application
3. Add environment variables in the Railway dashboard
4. Deploy!

## 🔍 Performance Optimizations

- **Database Indexing**: Indexes on frequently queried fields (name, sizes, user_id)
- **Async Operations**: All database operations are asynchronous
- **Connection Pooling**: Motor handles connection pooling automatically
- **Pagination**: Implemented to handle large datasets efficiently
- **Query Optimization**: Efficient MongoDB queries with proper filtering

## 🧪 Testing

The application includes comprehensive error handling and validation. Test the APIs using:
- Swagger UI at `/docs`
- Postman or similar API testing tools
- curl commands as shown in examples

## 🤝 Contributing

This is a hiring assignment project. The code follows best practices for:
- Clean code structure
- Comprehensive documentation
- Error handling
- Performance optimization
- Security considerations

## 📝 Notes

- All timestamps are stored in UTC
- Product inventory is automatically updated when orders are created
- The application includes proper error handling for edge cases
- MongoDB ObjectIds are converted to strings in API responses
- Partial text search is supported for product names (case-insensitive)

## 🔗 Links

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **MongoDB Motor Documentation**: https://motor.readthedocs.io/
- **Pydantic Documentation**: https://docs.pydantic.dev/
>>>>>>> e703c41 (Innitial)
