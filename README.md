## Recipes
Recipes is a prototype web app I built while learning Neo4j, a graph database. It is designed to help a user search a database of over 10,000 recipes and quickly find one that meets their criteria.

Recipes uses the python-based web framework Flask for server-side handling, HTML/CSS/JavaScript for the front-end, and the neo4j-provided bolt driver to connect to the database. The project is hosted on a Google Compute Engine VM. Contact me for url.

#### Components
The Recipes folder contains the Flask application including model, view, templates, and static files. The data folder contains source data for the recipes and a notebook for flattening the JSON into CSVs.

#### Data
The data for this project was provided by neo4j developer Mark Needham and can be found here https://raw.githubusercontent.com/mneedham/bbcgoodfood/master/stream_all.json. A load script was also provided, but I chose to create my own because the author’s script didn’t make use of all the available data. After downloading the source file, I imported it into a PANDAS DataFrame and generated a csv containing a record for each recipe and each of its scalar data properties. I then generated a csv for each of the other nodes. The data was then loaded through the neo4j cypher-shell. See recipes/data/data_prep.ipynb for details.

#### UI
The application provides a user interface for the database, abstracting out the implementation details while allowing the user to interact with the data. A user can search recipes, view information for any single recipe, and save recipes to their own dashboard. As this is only a demo, user accounts and changes in the database are not stored long-term and reset to the initial load at set intervals. 

#### Queries
All queries are written in one of four classes – User, Recipe, Ingredient, Collection. A driver object processes each query as a string and returns the result to the browser as a bolt object. Because the templating system used by the web framework uses a syntax similar to cypher, I primarily make use of the ’WHERE’ statement instead of using the shorthand nested syntax to avoid repeated escaping of braces in the query strings. All queries fall into one of the follwoing classifications.

Functional Queries
Queries performed by the system to present information to the user.
The majority of the queries fall into this category. These are often low-level queries that are templated across the classes and strung together to create larger queries.

Search Queries
Queries performed by the user to search the database of recipes.
These queries are accessed through the recipes page and allow the user get lists of recipes based on some input value. The results are returned to the recipes table. In general, I am not limiting the number of results and managing them by paging through the UI. This does cause some delay when the results set is large so I may add an ajax call instead.

Selection Queries
Queries performed by the user to work with individual recipes.
Once a recipe is selected and the detail page is loaded, the user has a limited number of options to interact with a recipe.