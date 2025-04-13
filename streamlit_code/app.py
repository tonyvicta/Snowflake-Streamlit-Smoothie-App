# import python packages 
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# App title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# First text input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of your Smoothie will be:' , name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Load table and convert to Pandas
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

# Ingredient selector
ingredients_List = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist()
)

# Optional name re-entry
name_on_order = st.text_input("Enter your name")

if ingredients_List:
    ingredients_string = ''

    for fruit_chosen in ingredients_List:
        ingredients_string += fruit_chosen + ' '
        st.subheader(f"{fruit_chosen} Nutrition Information")

        # ✅ Lookup the correct API name
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write(f"🔍 API search key: {search_on}")  # Optional debug

        # ✅ API request using SEARCH_ON
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)

        if smoothiefroot_response.ok:
            try:
                sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
            except requests.exceptions.JSONDecodeError:
                st.error("❌ The API response is not valid JSON.")
                st.text(smoothiefroot_response.text[:300])
        else:
            st.error(f"❌ API call failed with status {smoothiefroot_response.status_code}")

    # Insert into Snowflake
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string.strip()}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")

    st.stop()
