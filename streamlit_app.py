if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        # This subheader and dataframe will show for each fruit selected
        st.subheader(fruit_chosen + ' Nutrition Information')
        
        # Using fruit_chosen makes the API call dynamic for each selection
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # These lines must be aligned with the "for" loop to run after the loop finishes
    my_insert_stmt = (
        "INSERT INTO smoothies.public.ORDERS (ingredients, NAME_ON_ORDER) "
        "VALUES ('" + ingredients_string + "', '" + name_on_order + "')"
    )

    time_to_insert = st.button('Submit order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# sf = st.dataframe(data =smoothiefroot_response.json(),use_container_width=True)
