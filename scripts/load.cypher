USING PERIODIC COMMIT LOAD CSV FROM "file:///home/jdecker77/projects/recipes/resources/cleaning/output/recipes_all_clean.csv" AS row
MERGE (r:Recipe {id: toInteger(row[0])})
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
ON CREATE SET r.Fat = row[16];


USING PERIODIC COMMIT LOAD CSV FROM "file:///home/jdecker77/projects/recipes/resources/cleaning/output/ingredients.csv" AS row
MERGE (i:Ingredient {name:row[1]});

USING PERIODIC COMMIT LOAD CSV FROM "file:///home/jdecker77/projects/recipes/resources/cleaning/output/ingredients.csv" AS row
MATCH (r:Recipe), (i:Ingredient)
WHERE r.id = toInteger(row[0]) AND i.name = row[1]
CREATE (r)-[:CONTAINS]->(i);

USING PERIODIC COMMIT LOAD CSV FROM "file:///home/jdecker77/projects/recipes/resources/cleaning/output/diet_types.csv" AS row
MERGE (dt:DietType {name:row[1]});

USING PERIODIC COMMIT LOAD CSV FROM "file:///home/jdecker77/projects/recipes/resources/cleaning/output/diet_types.csv" AS row
MATCH (r:Recipe), (dt:DietType)
WHERE r.id = toInteger(row[0]) AND dt.name = row[1]
CREATE (r)-[:ISOFTYPE]->(dt);

USING PERIODIC COMMIT LOAD CSV FROM "file:///home/jdecker77/projects/recipes/resources/cleaning/output/author.csv" AS row
MERGE (a:Author {name:row[1]});

USING PERIODIC COMMIT LOAD CSV FROM "file:///home/jdecker77/projects/recipes/resources/cleaning/output/author.csv" AS row
MATCH (r:Recipe), (a:Author)
WHERE r.id = toInteger(row[0]) AND a.name = row[1]
CREATE (r)<-[:CREATEDBY]-(a);

USING PERIODIC COMMIT LOAD CSV FROM "file:///home/jdecker77/projects/recipes/resources/cleaning/output/courses.csv" AS row
MERGE (c:Course {name:row[1]});

USING PERIODIC COMMIT LOAD CSV FROM "file:///home/jdecker77/projects/recipes/resources/cleaning/output/courses.csv" AS row
MATCH (r:Recipe), (c:Course)
WHERE r.id = toInteger(row[0])  AND c.name = row[1]
CREATE (r)-[:CONSUMED]->(c);

USING PERIODIC COMMIT LOAD CSV FROM "file:///home/jdecker77/projects/recipes/resources/cleaning/output/collections.csv" AS row
MERGE (c:Collection {name:row[1]});

USING PERIODIC COMMIT LOAD CSV FROM "file:///home/jdecker77/projects/recipes/resources/cleaning/output/collections.csv" AS row
MATCH (r:Recipe), (c:Collection)
WHERE r.id = toInteger(row[0])  AND c.name = row[1]
CREATE (r)-[:ORGANIZEDINTO]->(c);

USING PERIODIC COMMIT LOAD CSV FROM "file:///home/jdecker77/projects/recipes/resources/cleaning/output/keywords.csv" AS row
MERGE (k:Keyword {name:row[1]});

USING PERIODIC COMMIT LOAD CSV FROM "file:///home/jdecker77/projects/recipes/resources/cleaning/output/keywords.csv" AS row
MATCH (r:Recipe), (k:Keyword)
WHERE r.id = toInteger(row[0])  AND k.name = row[1]
CREATE (r)-[:TAGGED]->(k);
