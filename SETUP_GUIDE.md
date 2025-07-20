# 🚀 Complete Setup Guide for E-Commerce Backend API

This guide will walk you through setting up and running the e-commerce backend API from scratch.

## 📋 Prerequisites

Before starting, ensure you have:
- Python 3.11 or higher installed
- Git installed
- A MongoDB Atlas account (free tier available)
- Basic knowledge of terminal/command line

## 🛠️ Step-by-Step Setup Instructions

### Step 1: Environment Setup

1. **Create a new directory for your project:**
\`\`\`bash
mkdir ecommerce-api-project
cd ecommerce-api-project
\`\`\`

2. **Create a Python virtual environment:**
\`\`\`bash
# On Windows
python -m venv venv
venv\\Scripts\\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
\`\`\`

3. **Verify Python version:**
\`\`\`bash
python --version
# Should show Python 3.11 or higher
\`\`\`

### Step 2: Install Dependencies

1. **Install required packages:**
\`\`\`bash
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install motor==3.3.2
pip install pymongo==4.6.0
pip install pydantic==2.5.0
pip install python-multipart==0.0.6
pip install python-dotenv==1.0.0
\`\`\`

2. **Verify installation:**
\`\`\`bash
pip list
\`\`\`

### Step 3: MongoDB Atlas Setup

1. **Create MongoDB Atlas Account:**
   - Go to https://www.mongodb.com/atlas
   - Sign up for a free account
   - Create a new project

2. **Create a Free Cluster:**
   - Click "Build a Database"
   - Choose "M0 Sandbox" (Free tier)
   - Select your preferred cloud provider and region
   - Name your cluster (e.g., "ecommerce-cluster")

3. **Configure Database Access:**
   - Go to "Database Access" in the left sidebar
   - Click "Add New Database User"
   - Choose "Password" authentication
   - Create username and password (save these!)
   - Set privileges to "Read and write to any database"

4. **Configure Network Access:**
   - Go to "Network Access" in the left sidebar
   - Click "Add IP Address"
   - Choose "Allow Access from Anywhere" (0.0.0.0/0)
   - Confirm the entry

5. **Get Connection String:**
   - Go to "Database" in the left sidebar
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace \`<password>\` with your actual password

### Step 4: Environment Configuration

1. **Create environment file:**
\`\`\`bash
# Create .env file in your project root
touch .env
\`\`\`

2. **Add configuration to .env file:**
\`\`\`env
MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/ecommerce_db?retryWrites=true&w=majority
DATABASE_NAME=ecommerce_system
PORT=8000
\`\`\`

Replace the connection string with your actual MongoDB Atlas connection string.

### Step 5: Copy Application Files

Copy all the provided Python files to your project directory:
- \`app.py\` (main application)
- \`schemas.py\` (data models)
- \`db_manager.py\` (database operations)
- \`test_data_generator.py\` (sample data)
- \`requirements.txt\` (dependencies)

### Step 6: Test the Setup

1. **Generate sample data:**
\`\`\`bash
python test_data_generator.py
\`\`\`

You should see output like:
\`\`\`
🚀 Generating sample data for E-Commerce API...
✅ MongoDB connection established successfully
🧹 Cleared existing test data
✅ Created 6 sample products
\`\`\`

2. **Start the application:**
\`\`\`bash
python app.py
\`\`\`

You should see:
\`\`\`
🚀 E-Commerce API System is ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
\`\`\`

3. **Test the API:**
   - Open your browser and go to: http://localhost:8000/health
   - You should see: \`{"service": "E-Commerce Backend API", "status": "operational", ...}\`

### Step 7: Explore the API

1. **Access API Documentation:**
   - Swagger UI: http://localhost:8000/api-docs
   - ReDoc: http://localhost:8000/api-documentation

2. **Test endpoints using curl:**

**Get all products:**
\`\`\`bash
curl http://localhost:8000/products
\`\`\`

**Create a new product:**
\`\`\`bash
curl -X POST "http://localhost:8000/products" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Test Product",
    "price": 19.99,
    "description": "A test product",
    "category": "Test",
    "inventory_count": 50,
    "sizes": ["medium", "large"]
  }'
\`\`\`

**Filter products by name:**
\`\`\`bash
curl "http://localhost:8000/products?name=shirt"
\`\`\`

**Create an order:**
\`\`\`bash
# First, get a product ID from the products list, then:
curl -X POST "http://localhost:8000/orders" \\
  -H "Content-Type: application/json" \\
  -d '{
    "user_id": "test_user_123",
    "items": [
      {
        "product_id": "YOUR_PRODUCT_ID_HERE",
        "quantity": 2,
        "price": 34.99
      }
    ],
    "total_amount": 69.98
  }'
\`\`\`

**Get user orders:**
\`\`\`bash
curl "http://localhost:8000/orders/test_user_123"
\`\`\`

## 🚀 Deployment Instructions

### Deploy to Render

1. **Prepare for deployment:**
   - Create a GitHub repository
   - Push your code to GitHub
   - Make sure \`requirements.txt\` is in the root directory

2. **Deploy on Render:**
   - Go to https://render.com
   - Sign up/login with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Build Command:** \`pip install -r requirements.txt\`
     - **Start Command:** \`uvicorn app:application --host 0.0.0.0 --port $PORT\`
   - Add environment variables:
     - \`MONGODB_CONNECTION_STRING\`: Your MongoDB Atlas connection string
     - \`DATABASE_NAME\`: ecommerce_system

3. **Test deployment:**
   - Once deployed, test your API at the provided Render URL
   - Example: https://your-app-name.onrender.com/health

### Deploy to Railway

1. **Deploy on Railway:**
   - Go to https://railway.app
   - Sign up/login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Python and deploy

2. **Add environment variables:**
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add your MongoDB connection string and database name

## 🧪 Testing Your API

### Using Swagger UI
1. Go to http://localhost:8000/api-docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the required parameters
5. Click "Execute"

### Using Postman
1. Download and install Postman
2. Create a new collection
3. Add requests for each endpoint
4. Test all CRUD operations

### Using Python requests
\`\`\`python
import requests

# Test health endpoint
response = requests.get("http://localhost:8000/health")
print(response.json())

# Get products
response = requests.get("http://localhost:8000/products")
print(response.json())
\`\`\`

## 🔧 Troubleshooting

### Common Issues:

1. **MongoDB Connection Error:**
   - Check your connection string
   - Verify network access settings in MongoDB Atlas
   - Ensure your IP is whitelisted

2. **Port Already in Use:**
   - Change the port in your .env file
   - Or kill the process using the port: \`lsof -ti:8000 | xargs kill -9\`

3. **Import Errors:**
   - Ensure all files are in the same directory
   - Check that your virtual environment is activated

4. **Validation Errors:**
   - Check the API documentation for required fields
   - Ensure data types match the schema requirements

## 📝 Next Steps

1. **Add Authentication:** Implement JWT tokens for user authentication
2. **Add More Features:** Categories, reviews, wishlist functionality
3. **Optimize Performance:** Add caching, database optimization
4. **Add Tests:** Write unit and integration tests
5. **Monitor:** Add logging and monitoring tools

## 🎯 Assignment Submission

For the HROne assignment:
1. Deploy your API to Render or Railway
2. Test all endpoints work correctly
3. Submit the base URL (without trailing slash)
4. Ensure your GitHub repository is public
5. Include this README in your submission

Example submission URL: \`https://your-app-name.onrender.com\`

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the error messages carefully
3. Ensure all dependencies are installed correctly
4. Verify your MongoDB Atlas setup

Good luck with your assignment! 🚀
\`\`\`
