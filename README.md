# Daily Deaths Monitor — Gaza

This Streamlit dashboard visualizes daily and cumulative deaths in Gaza, using open data provided by the **Tech For Palestine** collective via the [Palestine API](https://github.com/ummahrican/palestine-api).  
It was inspired by the [Genocide Monitor](https://genocidemonitor.com/) project.

---

## 🧩 Data Sources

The data are retrieved from the **[Palestine API](https://github.com/ummahrican/palestine-api)**, which provides open access to datasets compiled by the **[Tech For Palestine](https://techforpalestine.org/)** collective.

Primary sources include:
- Gaza Ministry of Health  
- Gaza Government Media Office  
- UN OCHA  

These statistics reflect casualties **directly attributable to the genocide in Gaza** and are updated regularly.

---

## 📊 Features

- 📈 Cumulative deaths curve  
- 🧍 Death distribution by category (children, women, seniors)  
- 📊 Casualties by age (bar chart)  
- 📅 Daily casualties table  

---

## 🎨 Theme configuration

This project includes a custom Streamlit configuration file (.streamlit/config.toml) defining a dark theme. This ensures visual consistency and readability across all elements of the dashboard.

---

## ⚙️ Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/gaza-daily-deaths-dashboard.git
cd gaza-daily-deaths-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run dashboard.py
```
---

## 💡 Acknowledgments

This project is inspired by the Genocide Monitor
