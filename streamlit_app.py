#First Streamlit Python App
import streamlit, pandas, requests, snowflake.connector
from urllib.error import URLError

streamlit.title("My New Python & Streamlit App");

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show);

# Defining a new function for API Request
def get_fruityvice_data(this_fruit_choide):
	fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choide)
	# streamlit.text(fruityvice_response.json()) # Prints pure JSON response
	fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
	return fruityvice_normalized;

# New Section to Display Fruityvice Api Reponse
streamlit.header("Fruityvice Fruit Advice!")
try:
	fruit_choice = streamlit.text_input('What fruit would you like information about?')
	if not fruit_choice:
		streamlit.error('Please enter a fruit to get information')
	else:
		streamlit.write('The user entered ', fruit_choice)
		back_from_function = get_fruityvice_data(fruit_choice)
		streamlit.dataframe(back_from_function)

except URLError as e:
		streamlit.error()

# Using Snowflake Connection Items
streamlit.header("The Fruit List At Snowflake ❄️")

# Snowflake-related functions
def get_fruit_load_list():
	with my_cnx.cursor() as my_cur:
		my_cur.execute("select * from fruit_load_list")
		return my_cur.fetchall()

# Adding a button to load the fruit
if streamlit.button('Get Fruit List'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	my_data_rows = get_fruit_load_list()
	my_cnx.close()
	streamlit.dataframe(my_data_rows)

# streamlit.stop() # pausing here while troubleshooting

# Allowing the end user to add a new fruit to the list
def insert_row_snowflake(new_fruit):
	with my_cnx.cursor() as my_cur:
		my_cur.execute("insert into FRUIT_LOAD_LIST values ('" + new_fruit + "')")
		return "New Fruit Added " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add Fruit to the List'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	back_from_function = insert_row_snowflake(add_my_fruit)
	my_cnx.close()
	streamlit.text(back_from_function)

