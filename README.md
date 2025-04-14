# 🥤 Smoothie Order App — Cloud Data & Streamlit Integration

This project builds a web-based smoothie order form using **Snowflake**, **Streamlit**, and **AWS**, including cloud data loading and UI interactivity.

---

## 🧰 Tech Stack
- Snowflake (Cloud Data Platform)
- Streamlit in Snowflake (SiS App)
- Amazon Web Services (AWS - trial account)
- Python
- SQL

---

## 📁 Project Structure

```
smoothie-order-app/
├── data/
│   └── fruits_available_for_smoothies.txt         # Raw fruit list file
│
├── snowflake_sql_scripts/
│   ├── 01_create_database.sql
│   ├── 02_create_fruit_options_table.sql
│   ├── 03_create_file_format.sql
│   ├── 04_load_stage_and_copy.sql
│   └── 05_query_table.sql
│
├── streamlit_code/
│   └── app.py                                      # Streamlit app
│
├── screenshots/
│   └── sis_app_preview.png                         # Screenshot from final email
│
└── README.md
```





[![Smoothie App](mysmoothie.png)](https://mysmoothie.streamlit.app/)
