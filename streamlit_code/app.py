# import python packages 
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# write directly to the app 
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of your Smoothie will be:' , name_on_order)

cnx = st. connection ("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options") .select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_List = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe
)

if ingredients_List:
    ingredients_string = ''

    for fruit_chosen in ingredients_List:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    
  #st.write(ingredients_string)

  my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')"""

  # st.write(my_insert_stmt)
 

  #st.write(my_insert_stmt)
  time_to_insert = st.button('Submit Order')

  if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")

  st.stop()


