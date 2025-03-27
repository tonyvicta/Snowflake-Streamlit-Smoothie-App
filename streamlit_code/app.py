🧑‍💻 Streamlit App (SiS App)
App Title: Custom Smoothie Order Form
App Location: SMOOTHIES.PUBLIC
Warehouse: COMPUTE_WH


import streamlit as st
from snowflake.snowpark.context import get_active_session

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

option = st.selectbox(
    "What is your favourite fruit?",
    ("Banana", "Strawberries", "Peaches"),
)
st.write("Your favourite fruit is:", option)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options")
st.dataframe(data=my_dataframe, use_container_width=True)
