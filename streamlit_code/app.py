🧑‍💻 Streamlit App (SiS App)
App Title: Custom Smoothie Order Form
App Location: SMOOTHIES.PUBLIC
Warehouse: COMPUTE_WH

import streamlit as st
from snowflake.snowpark.context import get_active_session

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

from snowflake.snowpark.functions import col

session = get_active_session()
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
 
  #st.write(ingredients_string)


  my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

  #st.write(my_insert_stmt)
  time_to_insert = st.button('Submit Order')

  if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
