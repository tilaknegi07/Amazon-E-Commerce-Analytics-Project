# Streamlit Quick Reference 🚀

Essential commands and tips for your dashboard

---

## 🎯 Local Development Commands

### Start the Dashboard
```bash
streamlit run app.py
```

### Start on Custom Port
```bash
streamlit run app.py --server.port 8502
```

### Start with Auto-reload (for development)
```bash
streamlit run app.py --server.runOnSave true
```

### Clear Cache
```bash
streamlit cache clear
```

---

## 📝 Common Streamlit Commands (In-Code)

### Page Config (MUST be first command)
```python
st.set_page_config(
    page_title="My Dashboard",
    page_icon="🛒",
    layout="wide",           # or "centered"
    initial_sidebar_state="expanded"  # or "collapsed"
)
```

### Text Elements
```python
st.title("Main Title")
st.header("Section Header")
st.subheader("Subsection")
st.markdown("**Bold** and *italic*")
st.text("Plain text")
st.code("print('Hello')", language="python")
```

### Data Display
```python
st.dataframe(df)                    # Interactive table
st.table(df)                        # Static table
st.metric("Revenue", "$1.2M", "+15%")  # KPI metric
st.json({"key": "value"})           # JSON viewer
```

### Charts (Built-in)
```python
st.line_chart(data)
st.bar_chart(data)
st.area_chart(data)
st.map(data)  # Requires lat/lon columns
```

### Charts (Plotly - Better!)
```python
import plotly.express as px
fig = px.bar(df, x='category', y='revenue')
st.plotly_chart(fig, use_container_width=True)
```

### Layout
```python
# Columns
col1, col2, col3 = st.columns(3)
with col1:
    st.write("Column 1")

# Sidebar
st.sidebar.title("Filters")
selected = st.sidebar.selectbox("Choose", options)

# Tabs
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
with tab1:
    st.write("Content")

# Expander
with st.expander("Show Details"):
    st.write("Hidden content")

# Container
with st.container():
    st.write("Grouped content")
```

### Input Widgets
```python
# Text input
name = st.text_input("Enter name")

# Number input
age = st.number_input("Age", min_value=0, max_value=120)

# Select box
choice = st.selectbox("Choose", ["A", "B", "C"])

# Multi-select
choices = st.multiselect("Choose multiple", ["A", "B", "C"])

# Slider
value = st.slider("Select", min_value=0, max_value=100)

# Date input
date = st.date_input("Select date")

# Checkbox
agree = st.checkbox("I agree")

# Radio buttons
option = st.radio("Choose one", ["Yes", "No"])

# File uploader
file = st.file_uploader("Upload CSV", type=['csv'])
```

### Feedback & Status
```python
st.success("Success message!")
st.info("Info message")
st.warning("Warning message")
st.error("Error message")
st.exception(e)  # Show exception

# Progress bar
progress = st.progress(0)
for i in range(100):
    progress.progress(i + 1)

# Spinner
with st.spinner("Loading..."):
    # long running code
    time.sleep(3)
```

### Caching (CRITICAL for Performance!)
```python
# Cache data loading
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

# Cache ML models
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

# Clear cache programmatically
st.cache_data.clear()
```

---

## 🎨 Styling Tips

### Custom CSS
```python
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
```

### Custom Colors (config.toml)
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

---

## 🔧 Debugging Tips

### Show Variables
```python
st.write(variable)  # Shows any Python object
st.json(dict)       # Pretty print dictionaries
```

### Debug Mode
```python
if st.checkbox("Show Debug Info"):
    st.write("DataFrame shape:", df.shape)
    st.write("Columns:", df.columns.tolist())
    st.write(df.head())
```

### Error Handling
```python
try:
    data = load_data()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()  # Stop execution
```

---

## 🚀 Performance Optimization

### DO's ✅
```python
# Cache expensive operations
@st.cache_data
def expensive_operation():
    return result

# Use use_container_width for responsive charts
st.plotly_chart(fig, use_container_width=True)

# Load only needed data
df = pd.read_csv("file.csv", usecols=['col1', 'col2'])

# Use st.spinner for long operations
with st.spinner("Processing..."):
    process_data()
```

### DON'Ts ❌
```python
# Don't load data on every rerun
# df = pd.read_csv("large_file.csv")  # Bad!

# Don't use print() (won't show up)
# print("Debug")  # Use st.write() instead

# Don't load entire dataset if not needed
# df = pd.read_csv("file.csv")  # Loads everything
```

---

## 📦 Deployment Checklist

Before deploying:
- [ ] All imports in requirements.txt
- [ ] Removed hardcoded paths
- [ ] No print() statements (use st.write())
- [ ] Added @st.cache_data to data loading
- [ ] Tested with sample data
- [ ] Added error handling
- [ ] Removed debug code
- [ ] Optimized for mobile (test in responsive mode)

---

## 🎓 Learn More

### Essential Resources
- **Docs:** https://docs.streamlit.io
- **Gallery:** https://streamlit.io/gallery
- **Cheat Sheet:** https://docs.streamlit.io/library/cheatsheet
- **Forum:** https://discuss.streamlit.io

### Example Apps
```python
# Run official examples
streamlit hello
```

---

## 🆘 Common Issues & Solutions

### Issue: "Requirements could not be installed"
**Solution:** Check requirements.txt for typos
```txt
streamlit==1.28.0  # Correct
stremalit==1.28.0  # Typo! Will fail
```

### Issue: "Module not found"
**Solution:** Add to requirements.txt
```txt
plotly==5.17.0
pandas==2.1.0
```

### Issue: App keeps rerunning
**Solution:** Use session_state
```python
if 'counter' not in st.session_state:
    st.session_state.counter = 0
```

### Issue: Charts not showing
**Solution:** Make sure to call st.plotly_chart()
```python
fig = px.bar(...)  # This creates the chart
st.plotly_chart(fig)  # This displays it!
```

### Issue: Slow performance
**Solution:** Add caching
```python
@st.cache_data
def load_data():
    return pd.read_csv("large_file.csv")
```

---

## 💡 Pro Tips

1. **Use session_state for persistence**
   ```python
   if 'data' not in st.session_state:
       st.session_state.data = load_data()
   ```

2. **Make it mobile-friendly**
   - Test on mobile (Chrome DevTools)
   - Use responsive columns
   - Keep charts clear on small screens

3. **Add loading indicators**
   ```python
   with st.spinner('Loading data...'):
       data = expensive_function()
   ```

4. **Show progress for long operations**
   ```python
   progress_bar = st.progress(0)
   for i in range(100):
       # do work
       progress_bar.progress(i + 1)
   ```

5. **Use fragments for partial updates** (New in Streamlit 1.30+)
   ```python
   @st.fragment
   def update_chart():
       # Only this reruns, not whole app
       st.plotly_chart(fig)
   ```

---

## 🎯 Quick Wins for Your Dashboard

### Add Download Button
```python
csv = df.to_csv(index=False)
st.download_button(
    "Download Data",
    csv,
    "data.csv",
    "text/csv"
)
```

### Add Dark Mode Toggle
```python
# In .streamlit/config.toml
[theme]
base = "dark"  # or "light"
```

### Add Filters That Persist
```python
if 'category' not in st.session_state:
    st.session_state.category = 'All'

category = st.selectbox(
    "Category",
    options=['All'] + list(df['category'].unique()),
    key='category'
)
```

---

## 📞 Getting Help

**Before asking:**
1. Check the docs
2. Search the forum
3. Look at example apps
4. Read error messages carefully

**When asking for help:**
- Share minimal code that reproduces the issue
- Include error messages
- Mention Streamlit version (`streamlit --version`)
- Describe what you expected vs. what happened

---

## ✅ Daily Workflow

**Morning:**
```bash
git pull
streamlit run app.py
# Make changes, see live updates
```

**During development:**
- Save file → Auto-reload
- Use st.write() for debugging
- Test filters and interactions
- Check mobile view

**Before committing:**
```bash
# Test the app
streamlit run app.py

# Commit and push
git add .
git commit -m "Add new feature"
git push

# Streamlit Cloud auto-deploys!
```

---

**Keep this file handy while building! 🚀**
