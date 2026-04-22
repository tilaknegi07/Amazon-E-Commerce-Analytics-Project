"""
Amazon E-Commerce Analytics Dashboard
Interactive Streamlit application for visualizing e-commerce insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Amazon E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #FF9900;
        font-weight: 700;
    }
    h2 {
        color: #232F3E;
        font-weight: 600;
    }
    h3 {
        color: #37475A;
        font-weight: 500;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 0 20px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF9900;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Data loading function with caching
@st.cache_data
def load_data():
    """
    Load and prepare sample data for the dashboard
    In production, this would connect to your PostgreSQL database
    """
    # Generate sample data (replace with actual database connection)
    np.random.seed(42)
    n_records = 10000
    
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports', 'Beauty', 'Toys']
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
    devices = ['Mobile', 'Desktop', 'Tablet']
    payment_methods = ['Credit Card', 'UPI', 'Cash on Delivery', 'Debit Card']
    delivery_statuses = ['Delivered', 'In Transit', 'Pending', 'Returned']
    brands = ['Brand A', 'Brand B', 'Brand C', 'Brand D', 'Brand E', 'Brand F', 'Brand G', 'Brand H']
    
    # Generate dates for the last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, periods=n_records)
    
    data = {
        'product_id': [f'PROD_{i:05d}' for i in range(n_records)],
        'category': np.random.choice(categories, n_records, p=[0.25, 0.20, 0.15, 0.10, 0.10, 0.10, 0.10]),
        'brand': np.random.choice(brands, n_records),
        'price': np.random.uniform(100, 5000, n_records).round(2),
        'discount': np.random.uniform(0, 40, n_records).round(2),
        'rating': np.random.uniform(1, 5, n_records).round(1),
        'purchase_date': dates,
        'location': np.random.choice(cities, n_records, p=[0.20, 0.18, 0.15, 0.12, 0.10, 0.10, 0.08, 0.07]),
        'device': np.random.choice(devices, n_records, p=[0.65, 0.25, 0.10]),
        'payment_method': np.random.choice(payment_methods, n_records, p=[0.35, 0.30, 0.20, 0.15]),
        'delivery_status': np.random.choice(delivery_statuses, n_records, p=[0.75, 0.10, 0.10, 0.05]),
        'seller_id': [f'SELLER_{np.random.randint(1, 50):03d}' for _ in range(n_records)],
        'is_returned': np.random.choice(['FALSE', 'TRUE'], n_records, p=[0.92, 0.08])
    }
    
    df = pd.DataFrame(data)
    
    # Calculate derived fields
    df['final_price'] = (df['price'] * (1 - df['discount'] / 100)).round(2)
    df['saving'] = (df['price'] - df['final_price']).round(2)
    df['price_bucket'] = pd.qcut(df['price'], q=4, labels=['Budget', 'Mid', 'Premium', 'Luxury'])
    
    return df

# Load data
df = load_data()

# Sidebar filters
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", width=200)
st.sidebar.title("🔍 Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['purchase_date'].min(), df['purchase_date'].max()),
    min_value=df['purchase_date'].min(),
    max_value=df['purchase_date'].max()
)

# Category filter
categories = ['All'] + sorted(df['category'].unique().tolist())
selected_category = st.sidebar.selectbox("Category", categories)

# City filter
cities = ['All'] + sorted(df['location'].unique().tolist())
selected_city = st.sidebar.selectbox("City", cities)

# Price bucket filter
price_buckets = ['All'] + df['price_bucket'].unique().tolist()
selected_price_bucket = st.sidebar.selectbox("Price Segment", price_buckets)

# Apply filters
filtered_df = df.copy()
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['purchase_date'] >= pd.Timestamp(date_range[0])) &
        (filtered_df['purchase_date'] <= pd.Timestamp(date_range[1]))
    ]
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
if selected_city != 'All':
    filtered_df = filtered_df[filtered_df['location'] == selected_city]
if selected_price_bucket != 'All':
    filtered_df = filtered_df[filtered_df['price_bucket'] == selected_price_bucket]

# Main dashboard
st.title("🛒 Amazon E-Commerce Analytics Dashboard")
st.markdown(f"**Data Period:** {filtered_df['purchase_date'].min().strftime('%Y-%m-%d')} to {filtered_df['purchase_date'].min().strftime('%Y-%m-%d')} | **Records:** {len(filtered_df):,}")

# KPI metrics
col1, col2, col3, col4, col5 = st.columns(5)

total_revenue = filtered_df['final_price'].sum()
total_orders = len(filtered_df)
avg_order_value = filtered_df['final_price'].mean()
return_rate = (filtered_df['is_returned'] == 'TRUE').sum() / len(filtered_df) * 100
avg_discount = filtered_df['discount'].mean()

with col1:
    st.metric(
        "Total Revenue",
        f"${total_revenue:,.0f}",
        delta=f"{len(filtered_df)} orders"
    )

with col2:
    st.metric(
        "Avg Order Value",
        f"${avg_order_value:.2f}",
        delta=f"{(avg_order_value / df['final_price'].mean() - 1) * 100:.1f}%"
    )

with col3:
    st.metric(
        "Return Rate",
        f"{return_rate:.1f}%",
        delta=f"{return_rate - 8:.1f}%" if return_rate < 8 else f"+{return_rate - 8:.1f}%",
        delta_color="inverse"
    )

with col4:
    st.metric(
        "Avg Discount",
        f"{avg_discount:.1f}%",
        delta=f"{filtered_df['saving'].sum():,.0f} saved"
    )

with col5:
    avg_rating = filtered_df['rating'].mean()
    st.metric(
        "Avg Rating",
        f"{avg_rating:.1f}/5.0",
        delta=f"{(avg_rating - 4.0):.1f}"
    )

st.markdown("---")

# Tabs for different analyses
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "📦 Category Analysis", 
    "🌍 Geographic Insights",
    "📈 Trends & Patterns",
    "🏢 Seller Performance"
])

with tab1:
    st.header("Executive Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by category
        category_revenue = filtered_df.groupby('category')['final_price'].sum().sort_values(ascending=False)
        fig = px.pie(
            values=category_revenue.values,
            names=category_revenue.index,
            title="Revenue Distribution by Category",
            color_discrete_sequence=px.colors.qualitative.Bold,
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Orders by device
        device_orders = filtered_df.groupby('device').size()
        fig = go.Figure(data=[
            go.Bar(
                x=device_orders.index,
                y=device_orders.values,
                marker_color=['#FF9900', '#146EB4', '#232F3E'],
                text=device_orders.values,
                textposition='auto'
            )
        ])
        fig.update_layout(
            title="Orders by Device",
            xaxis_title="Device Type",
            yaxis_title="Number of Orders",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Payment method distribution
        payment_dist = filtered_df.groupby('payment_method')['final_price'].sum().sort_values(ascending=True)
        fig = go.Figure(data=[
            go.Bar(
                y=payment_dist.index,
                x=payment_dist.values,
                orientation='h',
                marker_color='#FF9900',
                text=[f'${v:,.0f}' for v in payment_dist.values],
                textposition='auto'
            )
        ])
        fig.update_layout(
            title="Revenue by Payment Method",
            xaxis_title="Revenue ($)",
            yaxis_title="Payment Method",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Delivery status
        delivery_data = filtered_df.groupby('delivery_status').agg({
            'final_price': 'sum',
            'product_id': 'count'
        }).reset_index()
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Orders', 'Revenue'),
            specs=[[{'type': 'domain'}, {'type': 'domain'}]]
        )
        
        fig.add_trace(go.Pie(
            labels=delivery_data['delivery_status'],
            values=delivery_data['product_id'],
            name="Orders"
        ), 1, 1)
        
        fig.add_trace(go.Pie(
            labels=delivery_data['delivery_status'],
            values=delivery_data['final_price'],
            name="Revenue"
        ), 1, 2)
        
        fig.update_layout(title_text="Delivery Status Overview", height=400)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Category Performance Analysis")
    
    # Category metrics table
    category_metrics = filtered_df.groupby('category').agg({
        'product_id': 'count',
        'final_price': ['sum', 'mean'],
        'discount': 'mean',
        'rating': 'mean',
        'is_returned': lambda x: (x == 'TRUE').sum() / len(x) * 100
    }).round(2)
    
    category_metrics.columns = ['Orders', 'Revenue', 'AOV', 'Avg Discount %', 'Avg Rating', 'Return Rate %']
    category_metrics = category_metrics.sort_values('Revenue', ascending=False)
    category_metrics['Revenue'] = category_metrics['Revenue'].apply(lambda x: f'${x:,.2f}')
    category_metrics['AOV'] = category_metrics['AOV'].apply(lambda x: f'${x:.2f}')
    
    st.dataframe(category_metrics, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue vs Orders by category
        cat_data = filtered_df.groupby('category').agg({
            'final_price': 'sum',
            'product_id': 'count'
        }).reset_index()
        
        fig = px.scatter(
            cat_data,
            x='product_id',
            y='final_price',
            size='final_price',
            color='category',
            hover_data=['category'],
            labels={'product_id': 'Number of Orders', 'final_price': 'Total Revenue'},
            title="Category Performance: Revenue vs Volume"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Return rate by category
        return_data = filtered_df.groupby('category').apply(
            lambda x: (x['is_returned'] == 'TRUE').sum() / len(x) * 100
        ).sort_values(ascending=False)
        
        fig = go.Figure(data=[
            go.Bar(
                x=return_data.index,
                y=return_data.values,
                marker_color=['#e74c3c' if v > 10 else '#27ae60' for v in return_data.values],
                text=[f'{v:.1f}%' for v in return_data.values],
                textposition='auto'
            )
        ])
        fig.add_hline(y=10, line_dash="dash", line_color="red", 
                      annotation_text="10% Target")
        fig.update_layout(
            title="Return Rate by Category",
            xaxis_title="Category",
            yaxis_title="Return Rate (%)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Brand performance within selected category
    if selected_category != 'All':
        st.subheader(f"Brand Performance in {selected_category}")
        brand_data = filtered_df[filtered_df['category'] == selected_category].groupby('brand').agg({
            'final_price': 'sum',
            'product_id': 'count',
            'rating': 'mean'
        }).sort_values('final_price', ascending=False).head(10)
        
        fig = go.Figure(data=[
            go.Bar(
                name='Revenue',
                x=brand_data.index,
                y=brand_data['final_price'],
                yaxis='y',
                marker_color='#FF9900'
            ),
            go.Scatter(
                name='Avg Rating',
                x=brand_data.index,
                y=brand_data['rating'],
                yaxis='y2',
                mode='lines+markers',
                marker=dict(size=10, color='#146EB4'),
                line=dict(width=3)
            )
        ])
        
        fig.update_layout(
            title=f'Top 10 Brands in {selected_category}',
            xaxis=dict(title='Brand'),
            yaxis=dict(title='Revenue ($)', side='left'),
            yaxis2=dict(title='Average Rating', overlaying='y', side='right', range=[0, 5]),
            legend=dict(x=0.01, y=0.99),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Geographic Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by city
        city_revenue = filtered_df.groupby('location')['final_price'].sum().sort_values(ascending=False)
        
        fig = go.Figure(data=[
            go.Bar(
                x=city_revenue.values,
                y=city_revenue.index,
                orientation='h',
                marker=dict(
                    color=city_revenue.values,
                    colorscale='Viridis',
                    showscale=True
                ),
                text=[f'${v:,.0f}' for v in city_revenue.values],
                textposition='auto'
            )
        ])
        fig.update_layout(
            title="Revenue by City",
            xaxis_title="Total Revenue ($)",
            yaxis_title="City",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # City metrics
        city_metrics = filtered_df.groupby('location').agg({
            'product_id': 'count',
            'final_price': ['sum', 'mean'],
            'is_returned': lambda x: (x == 'TRUE').sum() / len(x) * 100
        }).round(2)
        
        city_metrics.columns = ['Orders', 'Revenue', 'AOV', 'Return Rate %']
        city_metrics = city_metrics.sort_values('Revenue', ascending=False)
        
        st.markdown("### City Performance Metrics")
        st.dataframe(city_metrics, use_container_width=True)
    
    # Top category per city
    st.subheader("Top Category by City")
    top_cat_city = filtered_df.groupby(['location', 'category'])['final_price'].sum().reset_index()
    top_cat_city = top_cat_city.loc[top_cat_city.groupby('location')['final_price'].idxmax()]
    
    fig = px.bar(
        top_cat_city.sort_values('final_price', ascending=False),
        x='location',
        y='final_price',
        color='category',
        title="Leading Category in Each City",
        labels={'final_price': 'Revenue ($)', 'location': 'City'},
        text='category'
    )
    fig.update_traces(textposition='inside')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("Trends & Patterns")
    
    # Daily revenue trend
    daily_revenue = filtered_df.groupby(filtered_df['purchase_date'].dt.date).agg({
        'final_price': 'sum',
        'product_id': 'count'
    }).reset_index()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=daily_revenue['purchase_date'],
            y=daily_revenue['final_price'],
            name="Revenue",
            line=dict(color='#FF9900', width=2),
            fill='tozeroy'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=daily_revenue['purchase_date'],
            y=daily_revenue['product_id'],
            name="Orders",
            line=dict(color='#146EB4', width=2, dash='dash')
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title="Daily Revenue and Orders Trend",
        xaxis_title="Date",
        height=400
    )
    fig.update_yaxes(title_text="Revenue ($)", secondary_y=False)
    fig.update_yaxes(title_text="Number of Orders", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly trend
        filtered_df['month'] = filtered_df['purchase_date'].dt.to_period('M').astype(str)
        monthly_data = filtered_df.groupby('month').agg({
            'final_price': 'sum',
            'product_id': 'count'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly_data['month'],
            y=monthly_data['final_price'],
            name='Revenue',
            marker_color='#FF9900'
        ))
        
        fig.update_layout(
            title="Monthly Revenue Trend",
            xaxis_title="Month",
            yaxis_title="Revenue ($)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Price bucket distribution over time
        price_trend = filtered_df.groupby([filtered_df['purchase_date'].dt.to_period('M').astype(str), 'price_bucket']).size().reset_index()
        price_trend.columns = ['month', 'price_bucket', 'orders']
        
        fig = px.area(
            price_trend,
            x='month',
            y='orders',
            color='price_bucket',
            title="Order Volume by Price Segment",
            labels={'orders': 'Number of Orders', 'month': 'Month'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap: Day of week vs Hour (if we had hour data)
    filtered_df['day_of_week'] = filtered_df['purchase_date'].dt.day_name()
    dow_orders = filtered_df.groupby('day_of_week').size().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )
    
    fig = go.Figure(data=go.Bar(
        x=dow_orders.index,
        y=dow_orders.values,
        marker_color=['#146EB4' if day in ['Saturday', 'Sunday'] else '#FF9900' for day in dow_orders.index],
        text=dow_orders.values,
        textposition='auto'
    ))
    fig.update_layout(
        title="Orders by Day of Week",
        xaxis_title="Day",
        yaxis_title="Number of Orders",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("Seller Performance")
    
    # Top sellers
    seller_metrics = filtered_df.groupby('seller_id').agg({
        'product_id': 'count',
        'final_price': ['sum', 'mean'],
        'rating': 'mean',
        'is_returned': lambda x: (x == 'TRUE').sum() / len(x) * 100
    }).round(2)
    
    seller_metrics.columns = ['Orders', 'Revenue', 'AOV', 'Avg Rating', 'Return Rate %']
    seller_metrics = seller_metrics.sort_values('Revenue', ascending=False).head(20)
    
    # Highlight above-average sellers
    avg_aov = filtered_df['final_price'].mean()
    seller_metrics['Performance'] = seller_metrics['AOV'].apply(
        lambda x: '🌟 Above Average' if x > avg_aov else '📊 Average'
    )
    
    st.dataframe(seller_metrics, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Seller performance scatter
        top_sellers = filtered_df.groupby('seller_id').agg({
            'final_price': ['sum', 'mean'],
            'product_id': 'count'
        }).reset_index()
        top_sellers.columns = ['seller_id', 'revenue', 'aov', 'orders']
        top_sellers = top_sellers.nlargest(20, 'revenue')
        
        fig = px.scatter(
            top_sellers,
            x='aov',
            y='revenue',
            size='orders',
            color='orders',
            hover_data=['seller_id'],
            title="Seller Performance: AOV vs Total Revenue",
            labels={'aov': 'Average Order Value ($)', 'revenue': 'Total Revenue ($)'},
            color_continuous_scale='Viridis'
        )
        fig.add_vline(x=avg_aov, line_dash="dash", line_color="red",
                     annotation_text=f"Avg AOV: ${avg_aov:.2f}")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top 10 sellers by revenue
        top_10_sellers = filtered_df.groupby('seller_id')['final_price'].sum().nlargest(10).sort_values()
        
        fig = go.Figure(data=[
            go.Bar(
                y=top_10_sellers.index,
                x=top_10_sellers.values,
                orientation='h',
                marker_color='#FF9900',
                text=[f'${v:,.0f}' for v in top_10_sellers.values],
                textposition='auto'
            )
        ])
        fig.update_layout(
            title="Top 10 Sellers by Revenue",
            xaxis_title="Total Revenue ($)",
            yaxis_title="Seller ID",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p><strong>Amazon E-Commerce Analytics Dashboard</strong> | Built with Streamlit & Plotly</p>
        <p>📊 Data updated in real-time | 🔒 Secure & Private</p>
        <p>GitHub: <a href='https://github.com/yourusername/amazon-ecommerce-analytics'>View Source Code</a></p>
    </div>
    """, unsafe_allow_html=True)
