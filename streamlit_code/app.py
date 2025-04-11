🧑‍💻 Streamlit App (SiS App)
App Title: Custom Smoothie Order Form
App Location: SMOOTHIES.PUBLIC
Warehouse: COMPUTE_WH

# import python packages 
import streamlit as st
from snowflake.snowpark.functions import col

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


🧑‍💻 Streamlit App (SiS App)
App Title: Pending Smoothie Orders
App Location: SMOOTHIES.PUBLIC
Warehouse: COMPUTE_WH

# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤 Pending Smoothie Orders 🥤")
st.write("Orders that need to be filled.")

# Get active Snowflake session
session = get_active_session()

# Get unfilled orders from Snowflake
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == 0).to_pandas()

# ✅ Display editable table with checkboxes
editable_df = st.data_editor(
    my_dataframe[["INGREDIENTS", "NAME_ON_ORDER", "ORDER_FILLED"]],
    use_container_width=True,
    disabled=["INGREDIENTS", "NAME_ON_ORDER"]  # prevent editing these columns
)

submitted = st.button('Submit')

if submitted:
    st.success("Someone clicked the button.", icon="👍")


