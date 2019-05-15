cat /Users/jessedecker/projects/recipes/resources/tmp.cypher | cypher-shell -u neo4j -p "bubs&hen" --format plain
cat /Users/jessedecker/projects/recipes/resources/load.cypher | cypher-shell -u neo4j -p "bubs&hen" --format plain

-- Delete nodes
MATCH (n)
DETACH DELETE n

-- Create constraints
CREATE CONSTRAINT ON (r:Recipe) ASSERT r.id IS UNIQUE;
CREATE CONSTRAINT ON (i:Ingredient) ASSERT i.name IS UNIQUE;
CREATE CONSTRAINT ON (c:Collection) ASSERT c.name IS UNIQUE;
CREATE CONSTRAINT ON (u:User) ASSERT u.username IS UNIQUE;
CREATE CONSTRAINT ON (dt:DietType) ASSERT dt.name IS UNIQUE;
CREATE CONSTRAINT ON (k:Keyword) ASSERT k.name IS UNIQUE;
CREATE CONSTRAINT ON (c:Course) ASSERT c.name IS UNIQUE;
CREATE CONSTRAINT ON (a:Author) ASSERT a.name IS UNIQUE;



-- Load recipes
LOAD CSV FROM "file:///Users/jessedecker/projects/recipes/resources/cleaning/output/recipes_all_clean.csv" AS row;
MERGE (r:Recipe {id: toInteger(row[0])});
ON CREATE SET r.title = row[1]
ON CREATE SET r.description = row[2]
ON CREATE SET r.skill_level = row[4]
ON CREATE SET r.cooking_time = row[5]
ON CREATE SET r.prep_time = row[6]
ON CREATE SET r.servings = row[7]
ON CREATE SET r.ratings = row[8]
ON CREATE SET r.post_date = row[9]
ON CREATE SET r.Added_Sugar = row[10]
ON CREATE SET r.Carbohydrates = row[11]
ON CREATE SET r.Calories = row[12]
ON CREATE SET r.Protein = row[13]
ON CREATE SET r.Salt = row[14]
ON CREATE SET r.Saturated_Fat = row[15]
ON CREATE SET r.Fat = row[16]




LOAD CSV FROM "file:///Users/jessedecker/projects/recipes/resources/cleaning/output/ingredients.csv" AS row
MERGE (i:Ingredient {name:row[1]})

LOAD CSV FROM "file:///Users/jessedecker/projects/recipes/resources/cleaning/output/ingredients.csv" AS row
MATCH (r:Recipe), (i:Ingredient)
WHERE r.id = toInteger(row[0]) AND i.name = row[1]
CREATE (r)-[:CONTAINS]->(i)

LOAD CSV FROM "file:///Users/jessedecker/projects/recipes/resources/cleaning/output/diet_types.csv" AS row
MERGE (dt:DietType {name:row[1]})

LOAD CSV FROM "file:///Users/jessedecker/projects/recipes/resources/cleaning/output/diet_types.csv" AS row
MATCH (r:Recipe), (dt:DietType)
WHERE r.id = toInteger(row[0]) AND dt.name = row[1]
CREATE (r)-[:ISOFTYPE]->(dt)

LOAD CSV FROM "file:///Users/jessedecker/projects/recipes/resources/cleaning/output/author.csv" AS row
MERGE (a:Author {name:row[1]})

LOAD CSV FROM "file:///Users/jessedecker/projects/recipes/resources/cleaning/output/author.csv" AS row
MATCH (r:Recipe), (a:Author)
WHERE r.id = toInteger(row[0]) AND a.name = row[1]
CREATE (r)<-[:CREATEDBY]-(a)

LOAD CSV FROM "file:///Users/jessedecker/projects/recipes/resources/cleaning/output/courses.csv" AS row
MERGE (c:Course {name:row[1]})

LOAD CSV FROM "file:///Users/jessedecker/projects/recipes/resources/cleaning/output/courses.csv" AS row
MATCH (r:Recipe), (c:Course)
WHERE r.id = toInteger(row[0])  AND c.name = row[1]
CREATE (r)-[:CONSUMED]->(c)

LOAD CSV FROM "file:///Users/jessedecker/projects/recipes/resources/cleaning/output/collections.csv" AS row
MERGE (c:Collection {name:row[1]})

LOAD CSV FROM "file:///Users/jessedecker/projects/recipes/resources/cleaning/output/collections.csv" AS row
MATCH (r:Recipe), (c:Collection)
WHERE r.id = toInteger(row[0])  AND c.name = row[1]
CREATE (r)-[:ORGANIZEDINTO]->(c)

LOAD CSV FROM "file:///Users/jessedecker/projects/recipes/resources/cleaning/output/keywords.csv" AS row
MERGE (k:Keyword {name:row[1]})

LOAD CSV FROM "file:///Users/jessedecker/projects/recipes/resources/cleaning/output/keywords.csv" AS row
MATCH (r:Recipe), (k:Keyword)
WHERE r.id = toInteger(row[0])  AND k.name = row[1]
CREATE (r)-[:TAGGED]->(k)


MATCH (r:Recipe)
WHERE r.id = 5874481
SET r.ratings = r.ratings +1

MATCH (r:Recipe), (u:User)
WHERE r.id = 5874481 AND u.name = 'henry'
CREATE (u)-[:LIKES]->(r)





WITH ['cheese','lemon'] AS ingredients
MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)


MATCH path = (:Person)-->(:Movie)<--(:Person)
WHERE any(n in nodes(path) WHERE n.name = 'Michael Douglas')
RETURN extract(n IN nodes(path)| coalesce(n.name, n.title))




MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
WITH r.id AS recipe, i.name, ['cheese','lemon'] AS ingredients
RETURN recipe 

filter(x IN ingredients WHERE x.name IN )



MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
WHERE ALL (x IN ['cheese','lemon'] WHERE x = i.name)
RETURN r.id
    
MATCH (m:Movie)<-[r:ACTED_IN]-(a:Person)
WITH m.title AS movie, collect({name: a.name, roles: r.roles}) AS cast
RETURN movie, filter(actor IN cast WHERE actor.name STARTS WITH "M")




MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
WITH collect(r) as recipes

WHERE ALL (x IN ['cheese','lemon'] WHERE x = i.name)

(r:Recipe)-[:CONTAINS]->(i:Ingredient)

WHERE i.name IN ingredients

-- match ingredient first
-- get list of rec ids 
WITH ['cheese','lemon'] AS ingredients
MATCH (i:Ingredient)
WHERE i.name in ingredients
WITH collect(i) as things
MATCH (r:Recipe)
WHERE ALL(i in things WHERE (r)-[:CONTAINS]->(i))
RETURN r

RETURN i




WITH ['Keanu Reeves', 'Hugo Weaving', 'Emil Eifrem'] as names
MATCH (p:Person)
WHERE p.name in names
WITH collect(p) as persons
MATCH (m:Movie)
WHERE ALL(p in persons WHERE (p)-[:ACTED_IN]->(m))
RETURN m




r.id as id, r.title AS title, r.description AS description, r.skill_level AS skill_level, r.ratings AS ratings, toInteger(r.cooking_time)/60 as cooking_time, toInteger(r.prep_time)/60 as prep_time, r.servings as servings


WITH ['cheese','butter'] as ingredients
WHERE i.name IN ingredients
RETURN r, filter()


any(x IN {} WHERE x.name = value)

r.id as id, r.title AS title, r.description AS description, r.skill_level AS skill_level, r.ratings AS ratings, toInteger(r.cooking_time)/60 as cooking_time, toInteger(r.prep_time)/60 as prep_time, r.servings as servings, filter(i.name IN ingredients)









MATCH (r:Recipe)
RETURN AVG(r.ratings) AS average


WHERE r.ratings AS Likes, average


MATCH ()-[d:delayed_by]->(c:Carrier)
RETURN c.name  AS Carrier, 
       AVG(toFloat(d.dep_delay)) As avg
    ORDER BY avg DESC
    LIMIT 10

WITH ["cheese",'lemon'] AS ingredients
MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
WHERE i.name IN ingredients
RETURN r.id 

CALL algo.degree("Recipe", "SAVED", {direction: "incoming", writeProperty: "Saves"})


CALL algo.degree.stream("Recipe", "SAVES", {direction: "incoming"})
YIELD nodeId, score
RETURN algo.asNode(nodeId).id AS name


UNWIND ["chicken","beer"] AS ingredients
MATCH (r:Recipe)-[:CONTAINS]->(ingredients)
RETURN r.id as id, r.title AS title;


UNWIND ["chicken","beer"] AS ingredients
FOREACH ingredients
RETURN "ho";

MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
WHERE i.name in tmp
RETURN r


-- Convert data type
MATCH (r:Recipe)
SET r.ratings = toInteger(r.ratings)

-- Return all
Match (n:Indicator) return properties(n), ID(n) 

MATCH (r:Recipe)
DETACH DELETE r


-- Drop any specific index
DROP INDEX ON :Recipe(id)
DROP INDEX ON :Ingredient(name)
DROP INDEX ON :Author(name)

-- Create index - ?
CREATE INDEX ON :Recipe(id);
CREATE INDEX ON :Ingredient(name);
CREATE INDEX ON :User(username)



MATCH (r:Recipe)
WHERE r.id = 
RETURN count(r) > 0 AS exists

MATCH (u:User)
WHERE u.username = {}
RETURN count(u) > 0 AS exists

MATCH (u:User)
        WHERE u.username = '{}'
        RETURN u.password as password


MATCH (r:Recipe)<-[l:LIKES]-(u:User)
WHERE r.id = 55405 AND u.username = 'henry'
RETURN COUNT(l) > 0 as user_likes





CREATE (u:User)
ON CREATE SET u.username= '{}'


MATCH (r:Recipe { id: 102539 })-[:CONTAINS]->(i:Ingredient)
RETURN i.name

MATCH (r:Recipe)-[r.CONTAINS]->(i:Ingredient)
WHERE r.id = 102539
RETURN i.name

-- QUERIES

MATCH (i:Ingredient)<-[rel:CONTAINS]-(r:Recipe)
RETURN i.title, count(rel) as recipes order by recipes desc

-- Find other recipes
MATCH (r:Recipe {id:'101233'})-[:CONTAINS]->(i:Ingredient)<-[:CONTAINS]-(rec:Recipe)
WITH rec, COUNT(*) as commonIngredients
RETURN rec.title, rec.id ORDER BY commonIngredients DESC 

LIMIT 10

MATCH (r:Recipe {id:'101233'})-[:CONTAINS]->(i:Ingredient)
RETURN i.name







DROP CONSTRAINT ON (u:User) ASSERT u.username IS UNIQUE


query = '''
            MATCH (r:Recipe) 
            WHERE r.id = {}
            RETURN r.title AS title
            '''.format(recipe_id)


