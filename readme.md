# Please install the following python dependencies to get started:

- pip install langchain[all]
- pip install Flask
- pip install pandas

## Steps to start the api server

- Install all the required dependencies
- Create a data folder in the root and add source_documents folder inside it
- Open the terminal and type & run 'python app.py'

## API endpoint for testing

`http://127.0.0.1:5000/api/v1/gtapQuery?query={Enter your query here}`

## Sample Queries

- `http://127.0.0.1:5000/gtapQuery?query=Give me rice production data of India from 2011 to 2020 in json format and name the key as 'indian_rice_production_2011_to_2020' so that I can build a bar graph, here rice is item, production is element, india is area and 2011 is the year.`

- `http://127.0.0.1:5000/gtapQuery?query=tell me the item name for item code 221`
