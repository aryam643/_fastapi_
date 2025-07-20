# HROne E-commerce Backend API

A FastAPI-based backend application built for the HROne Backend Intern task. It provides RESTful APIs for managing products and orders using MongoDB.

## Features

* Product Management: Create and list products with filtering
* Order Management: Create orders and view user order history
* MongoDB Integration: Async operations using Motor
* Data Validation: Request/response validation via Pydantic
* Filtering & Pagination
* Error Handling and Logging
* Auto-generated API Documentation

## API Endpoints

### Products

* `POST /products` — Create a product
* `GET /products` — List products with optional filters

### Orders

* `POST /orders` — Place a new order
* `GET /orders/{user_id}` — Get orders for a user

## Tech Stack

* FastAPI (Python 3.11+)
* MongoDB with Motor (async driver)
* Pydantic v2
* OpenAPI/Swagger for Docs

## Installation & Setup

### Prerequisites

* Python 3.11 or higher
* MongoDB Atlas or local instance

### Local Development

```bash
git clone <your-repo-url>
cd hrone-backend-assignment
pip install -r requirements.txt
```

Create a `.env` file:

```env
MONGODB_URL=your_connection_string
DATABASE_NAME=hrone_ecommerce
PORT=8000
```

Run the application:

```bash
python main.py
```

API available at `http://localhost:8000`

### (Optional) Seed Sample Data

```bash
python scripts/seed_data.py
```

## API Documentation

* Swagger UI: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

## Usage Examples

### Create Product

```bash
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "T-Shirt", "price": 29.99, "inventory_count": 100, "sizes": ["M", "L"]}'
```

### Filter Products

```bash
curl "http://localhost:8000/products?name=shirt&size=L"
```

### Place Order

```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "items": [{"product_id": "xyz", "quantity": 2, "price": 29.99}], "total_amount": 59.98}'
```

### Get Orders

```bash
curl "http://localhost:8000/orders/user123"
```

## Project Structure

```
hrone-backend-assignment/
├── main.py
├── models.py
├── database.py
├── config.py
├── requirements.txt
├── Dockerfile
├── README.md
└── scripts/
    └── seed_data.py
```

## MongoDB Schema

### Products

```json
{
  "_id": "ObjectId",
  "name": "string",
  "price": "number",
  "description": "string",
  "category": "string",
  "inventory_count": "number",
  "sizes": ["S", "M", "L"],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Orders

```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "items": [{"product_id": "string", "quantity": "number", "price": "number"}],
  "total_amount": "number",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Deployment

### Render / Railway

1. Connect GitHub repo
2. Add environment variables
3. Start with:

   ```bash
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

## Performance Notes

* Indexed fields: `name`, `sizes`, `user_id`
* All DB operations are async
* Pagination support
* Motor handles connection pooling

## Testing

* Use Swagger UI or Postman
* Use provided curl examples

## Notes

* Timestamps in UTC
* Inventory updated automatically when orders are placed
* MongoDB ObjectIds converted to strings in responses
* Case-insensitive search supported on product name

---

### ✅ Now what?

To finish the rebase:

1. Save this cleaned-up content as `README.md`
2. Then run:

```bash
git add README.md
git rebase --continue
```
