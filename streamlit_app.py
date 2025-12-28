import streamlit as st
from snowflake.snowpark.functions import col
import requests

st.title(":cup_with_straw: Customize Your Smoothie!")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on smoothie:")

cnx = st.connection("snowflake")
session = cnx.session()

# SEARCH_ON column ko select karna zaroori hai
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        # SEARCH_ON value ko filter karke nikalna
        search_on_val = my_dataframe.filter(col("FRUIT_NAME") == fruit_chosen).select(col("SEARCH_ON")).collect()[0][0]
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        
        # API call mein SEARCH_ON variable ka istemal
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on_val)
        
        # Dataframe tabhi dikhega jab indentation (spacing) sahi ho
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = (
        "INSERT INTO smoothies.public.ORDERS (ingredients, NAME_ON_ORDER) "
        "VALUES ('" + ingredients_string + "', '" + name_on_order + "')"
    )

    time_to_order = st.button('Submit order')
    
    if time_to_order:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")# import requests
# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# sf = st.dataframe(data =smoothiefroot_response.json(),use_container_width=True)
