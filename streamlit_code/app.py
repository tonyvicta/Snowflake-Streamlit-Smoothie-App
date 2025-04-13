# import python packages 
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# write directly to the app 
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of your Smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert to pandas for filtering
pd_df = my_dataframe.to_pandas()

# Ingredient selector
ingredients_List = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist()
)

# Second name input field (optional to keep — can be removed)
# name_on_order = st.text_input("Enter your name")

if ingredients_List:
    ingredients_string = ''

    # Fetch all fruit data once
    response = requests.get("https://my.smoothiefroot.com/api/fruit/all")

    if response.ok:
        try:
            all_fruit_data = response.json()

            for fruit_chosen in ingredients_List:
                ingredients_string += fruit_chosen + ' '

                # Get the search slug from your Snowflake table
                search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

                # Find the matching fruit data in the full API response
                fruit_data = next((item for item in all_fruit_data if item["name"].lower() == search_on.lower()), None)

                st.subheader(f"{fruit_chosen} Nutrition Information")

                if fruit_data:
                    st.dataframe(data=fruit_data, use_container_width=True)
                else:
                    st.warning(f"⚠️ No data found for {fruit_chosen} (search key: {search_on})")

        except requests.exceptions.JSONDecodeError:
            st.error("❌ API returned invalid JSON.")
    else:
        st.error(f"❌ Could not fetch data. Status code: {response.status_code}")

    # Insert into orders table
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string.strip()}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")

    st.stop()
