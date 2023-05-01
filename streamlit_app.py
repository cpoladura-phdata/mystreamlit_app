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

# New Section to Display Fruityvice Api Reponse
streamlit.header("Fruityvice Fruit Advice!")
try:
	fruit_choice = streamlit.text_input('What fruit would you like information about?')
	if not fruit_choice:
		streamlit.write('Please enter a fruit to get information')
	else:
		streamlit.write('The user entered ', fruit_choice)

		fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
		# streamlit.text(fruityvice_response.json()) -Prints pure JSON response

		# normalizes the JSON response & writes the JSON into a table
		fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
		streamlit.dataframe(fruityvice_normalized)

except URLError as e:
		streamlit.error()

streamlit.stop() # pausing here while troubleshooting

# Using Snowflake Connection Items
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)
streamlit.header("The Fruit Load List Contains")
streamlit.dataframe(my_data_rows)

# allowing the end user to add a new fruit to the list
new_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('User looking to add ', new_fruit)

my_cur.execute("insert into FRUIT_LOAD_LIST values ('From Streamlit')")