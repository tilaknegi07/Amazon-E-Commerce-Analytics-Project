# Amazon E-Commerce Analytics Project 🛒📊

A comprehensive end-to-end data analytics project analyzing Amazon e-commerce transactions with over 1 million records. This project demonstrates the complete data analytics pipeline from data exploration to visualization using Python, SQL, and Power BI.

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Analysis Components](#analysis-components)
- [Key Insights](#key-insights)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Project Overview

This project performs an in-depth analysis of Amazon e-commerce data to uncover actionable business insights. The analysis covers multiple dimensions including:
- Revenue patterns and trends
- Product category performance
- Customer behavior analysis
- Geographic distribution
- Seller performance metrics
- Return rate analysis

## 📊 Dataset

**Dataset Size:** ~1 Million records

**Key Features:**
- `product_id`: Unique product identifier
- `category`: Product category
- `brand`: Product brand name
- `price`: Original product price
- `final_price`: Price after discount
- `discount`: Discount percentage
- `rating`: Product rating
- `purchase_date`: Date of purchase
- `location`: Customer city/location
- `device`: Device used for purchase
- `payment_method`: Payment method used
- `delivery_status`: Order delivery status
- `seller_id`: Seller identifier
- `is_returned`: Return status (TRUE/FALSE)

## 🛠 Tech Stack

### Data Processing & Analysis
- **Python 3.x**
  - pandas - Data manipulation and analysis
  - numpy - Numerical operations
  - matplotlib - Data visualization
  - seaborn - Statistical visualizations

### Database
- **PostgreSQL** - Relational database for data storage and complex queries

### Visualization & Reporting
- **Power BI** - Interactive dashboards and business intelligence

### Development Environment
- **Jupyter Notebook** - Interactive Python development

## 🏗 Project Architecture

```
Data Source (CSV)
       ↓
Python (Pandas) → Data Cleaning & Feature Engineering
       ↓
PostgreSQL Database → Advanced SQL Analytics
       ↓
Power BI → Interactive Dashboards & Reports
```

## 🔍 Analysis Components

### 1. Python Analysis (`Amazon_e-Commerce.ipynb`)

**Data Exploration:**
- Initial data inspection and quality assessment
- Statistical summary of numerical and categorical features
- Missing value analysis

**Data Transformation:**
- Date conversion for temporal analysis
- Feature engineering:
  - `Saving` = `price` - `final_price`
  - `price_bucket` = Quartile-based price categorization (Budget, Mid, Premium, Luxury)

**Exploratory Data Analysis:**
- Device-wise product distribution
- Payment method analysis
- Basic statistical profiling

**Database Integration:**
- Automated data loading to PostgreSQL using SQLAlchemy
- Connection parameters configured for local PostgreSQL instance

### 2. SQL Analysis (`amazon_e-commerce.sql`)

**Revenue Metrics (Section B)**
- **Overall Revenue Snapshot:**
  - Total orders, gross revenue, net revenue
  - Average order value (AOV), min/max order values
  - Total and average discount metrics
  - Overall discount percentage

- **Return Impact Analysis:**
  - Revenue split by returned vs. non-returned orders
  - Return rate impact on revenue

**Category & Subcategory Analysis (Section C)**
- Revenue distribution by category
- Category-wise order counts and average order values
- Revenue share percentage per category
- Returned vs. realized revenue by category
- Return revenue percentage by category

**Brand Performance (Section D)**
- Brand-wise revenue and order metrics
- Average order value by brand
- Brand-wise discount patterns
- Product ratings correlate with brand performance
- Return counts by brand

**Advanced Analytics with Window Functions (Section E)**
- **Revenue Ranking:**
  - RANK() and DENSE_RANK() for category revenue
  
- **Running Totals:**
  - Cumulative revenue over time ordered by purchase date
  
- **Customer Value Segmentation:**
  - Revenue analysis by price bucket tiers

**Geographic Analysis (Section F)**
- **City-Level Metrics:**
  - Orders and revenue by city
  - Average order value per city
  - Revenue share percentage by location
  - Return counts by city

- **Top Category per City:**
  - Identifying leading product categories in each location
  - Using PARTITION BY for location-specific rankings

**Seller Analysis (Section G)**
- Seller-wise average order value (AOV)
- Comparison against overall AOV
- High-performing sellers (above-average AOV)

**Risk Analysis**
- Revenue at risk by delivery status
- Correlation between delivery status and returns
- Already returned orders by delivery status

### 3. Power BI Dashboard (`amazon_e_commerce.pbix`)

Interactive visualizations, including:
- Executive summary dashboard with KPIs
- Category and brand performance charts
- Geographic heatmaps
- Time series analysis
- Return rate trends
- Seller performance scorecards

## 💡 Key Insights

Based on the SQL analysis structure, this project provides insights into:

1. **Revenue Optimization**
   - Identification of high-revenue categories and brands
   - Discount strategy effectiveness
   - Price sensitivity analysis across segments

2. **Customer Behavior**
   - Geographic purchasing patterns
   - Device preferences
   - Payment method preferences

3. **Operational Efficiency**
   - Return rate patterns by category/brand/location
   - Delivery status impact on customer satisfaction
   - Revenue at risk identification

4. **Seller Performance**
   - High-performing sellers vs. market average
   - Seller contribution to overall revenue

## 🚀 Installation & Setup

### Prerequisites
```bash
- Python 3.7+
- PostgreSQL 12+
- Power BI Desktop (for viewing .pbix file)
```

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/amazon-ecommerce-analytics.git
cd amazon-ecommerce-analytics
```

### Step 2: Install Python Dependencies
```bash
pip install pandas numpy matplotlib seaborn psycopg2-binary sqlalchemy
```

### Step 3: Database Setup
```sql
-- Create database in PostgreSQL
CREATE DATABASE Amazon_e-commerce;
```

### Step 4: Configure Database Connection
Update the connection parameters in the Jupyter notebook:
```python
username = "your_username"
password = "your_password"
host = "localhost"
port = 5432
database = "amazone_e-commerce"
```

### Step 5: Load Data
Run the Jupyter notebook cells to:
1. Load the CSV file
2. Clean and transform the data
3. Load data into PostgreSQL

### Step 6: Execute SQL Queries
Run the SQL queries in `amazon_e-commerce.sql` using your preferred PostgreSQL client (pgAdmin, DBeaver, etc.)

### Step 7: View Power BI Dashboard
Open `amazon_e_commerce.pbix` in Power BI Desktop to explore interactive visualizations.

## 📖 Usage

### Running Python Analysis
```bash
jupyter notebook Amazon_e-Commerce.ipynb
```

### Executing SQL Queries
```bash
psql -U postgres -d amazone_e-commerce -f amazon_e-commerce.sql
```

### Sample Queries

**Get top 5 revenue-generating categories:**
```sql
SELECT category, ROUND(SUM(final_price)::numeric, 2) AS net_revenue
FROM customers
GROUP BY category
ORDER BY net_revenue DESC
LIMIT 5;
```

**Analyze return impact:**
```sql
SELECT is_returned,
       COUNT(*) as orders,
       ROUND(SUM(final_price)::numeric, 2) as revenue
FROM customers
GROUP BY is_returned;
```

## 📁 Project Structure

```
amazon-ecommerce-analytics/
│
├── Amazon_e-Commerce.ipynb          # Python analysis notebook
├── amazon_e-commerce.sql            # SQL queries for analytics
├── amazon_e_commerce.pbix           # Power BI dashboard
├── data/
│   └── amazon_ecommerce_1M.csv      # Raw dataset (not included)
├── screenshots/                      # Dashboard screenshots
├── README.md                         # Project documentation
└── requirements.txt                  # Python dependencies
```

## 🔮 Future Enhancements

- [ ] Implement predictive models for sales forecasting
- [ ] Add customer segmentation using clustering algorithms
- [ ] Create automated reporting pipeline
- [ ] Integrate real-time data streaming
- [ ] Add sentiment analysis on product reviews
- [ ] Build a recommendation system for products
- [ ] Implement anomaly detection for fraud prevention
- [ ] Create API for data access
- [ ] Add more granular temporal analysis (hourly, seasonal)
- [ ] Integrate with cloud platforms (AWS, Azure, GCP)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 📄 License

This project is licensed under the MIT License 

---

**Note:** This project is for educational and portfolio purposes. The dataset used is synthetic/sample data and does not represent actual Amazon transactions.


⭐ **If you found this project helpful, please consider giving it a star!** ⭐
