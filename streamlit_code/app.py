# import python packages 
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# write directly to the app 
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of your Smoothie will be:' , name_on_order)

cnx = st.connection ("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()

ingredients_List = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe
)

name_on_order = st.text_input("Enter your name")

if ingredients_List:
    ingredients_string = ''

for fruit_chosen in ingredients_List:
    ingredients_string += fruit_chosen + ' '
    st.subheader(f"{fruit_chosen} Nutrition Information")

    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)

    if smoothiefroot_response.ok:
        try:
            sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        except requests.exceptions.JSONDecodeError:
            st.error("❌ The API response is not valid JSON.")
            st.text(smoothiefroot_response.text[:300])  # Optional debug
    else:
        st.error(f"❌ API call failed with status {smoothiefroot_response.status_code}")

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string.strip()}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")

    st.stop()
