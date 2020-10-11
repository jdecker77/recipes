from neo4j import GraphDatabase
import os
import sys
from passlib.hash import bcrypt
import datetime


class Driver(object):
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def RunQuery(self,query):
        with self.driver.session() as session:
            return session.run(query)

def GetDBDriver():
    drvr = None
    try:
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
        PROJ_ROOT = APP_ROOT.replace('Recipes','')

        with open(os.path.join(PROJ_ROOT, 'config.txt')) as infile:
            keys = infile.read().split('\n')

        # URL = 'bolt://recipes:7687'
        # bolt://localhost:7687
        URL = keys[0]
        USER = keys[1]
        PASS = keys[2]
        # print('url:',URL)
        # print('user:',USER)
        # print('pass:',PASS)

        drvr = Driver(URL,USER,PASS)

    except Exception as e:
        print(e,file=sys.stderr)
        print('Could not get rest api.')

    return drvr

driver = GetDBDriver()

''' 
User Class
'''
class User:
    def __init__(self, username):
        self.username = username

    def IsUser(self):
        query='''
        MATCH (u:User)
        WHERE u.username = '{}'
        RETURN count(u) > 0 AS exists
        '''.format(self.username)
        return driver.RunQuery(query)  

    def find(self):
        query='''
        MATCH (u:User)
        WHERE u.username = '{}'
        RETURN count(u) > 0 AS exists, u.password as password
        '''.format(self.username)
        return driver.RunQuery(query)

    def register(self, password):
        if self.find().single():
            return False
        else:
            usnm=self.username
            pswd=bcrypt.encrypt(password)
            query="CREATE (u:User {{username: '{}', password: '{}' }})".format(usnm,pswd)
            driver.RunQuery(query)
            return True
            
    def verify_password(self, password):
        if self.find().single()['exists']:
            pswd = self.find().single()['password']
            return bcrypt.verify(password, pswd)
        else:
            return False

    def LikeRecipe(self,recipe):
        query='''
        MATCH (r:Recipe), (u:User)
        WHERE r.id = {} AND u.username = '{}'
        CREATE (u)-[:LIKES]->(r)
        '''.format(recipe,self.username)
        driver.RunQuery(query)

    def SaveRecipe(self,recipe):
        query='''
        MATCH (r:Recipe), (u:User)
        WHERE r.id = {} AND u.username = '{}'
        CREATE (u)-[:SAVED]->(r)
        '''.format(recipe,self.username)
        driver.RunQuery(query)

    def RemoveRecipe(self,recipe):
        query='''
        MATCH (r:Recipe)<-[s:SAVED]-(u:User)
        WHERE r.id = {} AND u.username = '{}'
        DELETE s
        '''.format(recipe,self.username)
        driver.RunQuery(query)

    def GetSaved(self):
        query='''
        MATCH (r:Recipe)<-[:SAVED]-(u:User)
        WHERE u.username = '{}'
        RETURN r.id as id, r.title AS title, r.description AS description, r.skill_level AS skill_level, r.ratings AS ratings, toInteger(r.cooking_time)/60 as cooking_time, toInteger(r.prep_time)/60 as prep_time, r.servings as servings
        '''.format(self.username)
        return driver.RunQuery(query)


'''
Recipe Class
'''
class Recipe:
    def __init__(self, id):
        self.id = id

    def IsRecipe(self):
        query='''
        MATCH (r:Recipe)
        WHERE r.id = {}
        RETURN count(r) > 0 AS exists
        '''.format(self.id)
        return driver.RunQuery(query)    

    def get_list_of_recipes():
        query = '''
        MATCH (r:Recipe)
        RETURN r.id as id, r.title AS title, r.description AS description, r.skill_level AS skill_level, r.ratings AS ratings, toInteger(r.cooking_time)/60 as cooking_time, toInteger(r.prep_time)/60 as prep_time, r.servings as servings
        '''
        return driver.RunQuery(query)

    def GetRecipeByID(self):
        query='''
        MATCH (r:Recipe)
        WHERE r.id = {}
        RETURN r.id as id, r.title AS title, r.description AS description, r.skill_level AS skill_level, r.ratings AS ratings, toInteger(r.cooking_time)/60 as cooking_time, toInteger(r.prep_time)/60 as prep_time, r.servings as servings
        '''.format(self.id)
        return driver.RunQuery(query)

    def GetLike(self):
        query='''
        MATCH (r:Recipe)
        WHERE r.id = {}
        RETURN r.ratings as ratings
        '''.format(self.id)
        return driver.RunQuery(query)

    def GetRecipesBySkill(skill_level):
        query='''
        MATCH (r:Recipe)
        WHERE r.skill_level = '{}'
        RETURN r.id as id, r.title AS title, r.description AS description, r.skill_level AS skill_level, r.ratings AS ratings, toInteger(r.cooking_time)/60 as cooking_time, toInteger(r.prep_time)/60 as prep_time, r.servings as servings
        '''.format(skill_level)
        return driver.RunQuery(query)

    def GetRecipesByKeyword(keyword):
        query='''
        MATCH (r:Recipe)-[:TAGGED]->(k:Keyword)
        WHERE k.name = '{}'
        RETURN r.id as id, r.title AS title, r.description AS description, r.skill_level AS skill_level, r.ratings AS ratings, toInteger(r.cooking_time)/60 as cooking_time, toInteger(r.prep_time)/60 as prep_time, r.servings as servings
        '''.format(keyword)
        return driver.RunQuery(query)

    def GetRecipesByTotalTime(TotalTime,gt):
        query='''
        MATCH (r:Recipe)
        WHERE toInteger(r.cooking_time)/60 + toInteger(r.prep_time)/60 < {} and toInteger(r.cooking_time)/60 + toInteger(r.prep_time)/60 > {}
        RETURN r.id as id, r.title AS title, r.description AS description, r.skill_level AS skill_level, r.ratings AS ratings, toInteger(r.cooking_time)/60 as cooking_time, toInteger(r.prep_time)/60 as prep_time, r.servings as servings
        '''.format(TotalTime,gt)
        return driver.RunQuery(query)

    def GetRecipesByTopRating():
        query='''
        MATCH (r:Recipe)
        RETURN AVG(r.ratings) AS average
        '''
        average = driver.RunQuery(query).single()['average']
        average = average + average *.25

        query='''
        MATCH (r:Recipe)
        WHERE r.ratings > {}
        RETURN r.id as id, r.title AS title, r.description AS description, r.skill_level AS skill_level, r.ratings AS ratings, toInteger(r.cooking_time)/60 as cooking_time, toInteger(r.prep_time)/60 as prep_time, r.servings as servings
        '''.format(average)
        return driver.RunQuery(query)

    # Recipes that have been rated/liked in last 30 days
    def GetRecipesByTopSaved():
        query='''
        MATCH (r:Recipe)<-[:SAVED]-(u:User)
        RETURN r.id as id, r.title AS title, r.description AS description, r.skill_level AS skill_level, r.ratings AS ratings, toInteger(r.cooking_time)/60 as cooking_time, toInteger(r.prep_time)/60 as prep_time, r.servings as servings
        '''
        return driver.RunQuery(query)


    def GetKeywordsByRecipe(self):
        query='''
        MATCH (r:Recipe)-[:TAGGED]->(k:Keyword)
        WHERE r.id = {}
        RETURN k.name as name
        '''.format(self.id)
        return driver.RunQuery(query)

    def GetCoursesByRecipe(self):
        query='''
        MATCH (r:Recipe)-[:CONSUMED]->(c:Course)
        WHERE r.id = {}
        RETURN c.name as name
        '''.format(self.id)
        return driver.RunQuery(query)


    def GetIngredientsByRecipe(self):
        query = '''
        MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
        WHERE r.id = {}
        RETURN i.name AS name, r.id AS id
        '''.format(self.id)
        return driver.RunQuery(query)


    def GetAuthorByRecipe(self):
        query = '''
        MATCH (a:Author)-[:CREATEDBY]->(r:Recipe)
        WHERE r.id = {}
        RETURN a.name as author
        '''.format(self.id)
        return driver.RunQuery(query)

    def GetSkillByRecipe(self):
        query = '''
        MATCH (r:Recipe)
        WHERE r.id = {}
        RETURN r.skill_level as skill_level
        '''.format(self.id)
        return driver.RunQuery(query)

    def GetDietByRecipe(self):
        query = '''
        MATCH (r:Recipe)-[:ISOFTYPE]->(dt:DietType)
        WHERE r.id = {}
        RETURN dt.name as diet_type
        '''.format(self.id)
        return driver.RunQuery(query)


    def GetCollectionsByRecipe(self):
        query = '''
        MATCH (r:Recipe)-[:ORGANIZEDINTO]->(c:Collection)
        WHERE r.id = {}
        RETURN c.name as name
        '''.format(self.id)
        return driver.RunQuery(query)

    def GetCreatedDate(self):
        query = '''
        MATCH (r:Recipe)
        WHERE r.id = {}
        RETURN r.post_date as post_date
        '''.format(self.id)
        tmp = driver.RunQuery(query).single()['post_date']

        t = datetime.datetime.fromtimestamp(float(tmp)/1000.)

        fmt = "%Y-%m-%d %H:%M:%S"
        c_date = t.strftime(fmt)
        return  c_date

    # Get recipe by list of ingredients
    def GetRecipesByIngredients(search_query):  
        query = '''
        WITH {} AS ingredients
        MATCH (i:Ingredient)
        WHERE i.name in ingredients
        WITH collect(i) as things
        MATCH (r:Recipe)
        WHERE ALL(i in things WHERE (r)-[:CONTAINS]->(i))
        RETURN r.id as id, r.title AS title, r.description AS description, r.skill_level AS skill_level, r.ratings AS ratings, toInteger(r.cooking_time)/60 as cooking_time, toInteger(r.prep_time)/60 as prep_time, r.servings as servings
        '''.format(search_query)
        return driver.RunQuery(query)

    def GetNutritionByRecipe(self):
        query = '''
        MATCH (r:Recipe)
        WHERE r.id = {}
        RETURN r.Calories AS Calories,r.Carbohydrates AS Carbohydrates, r.Protein AS Protein,  r.Added_Sugar AS Sugar, r.Salt AS Salt, r.Fat AS Fat, r.Saturated_Fat AS Saturated_Fat
        '''.format(self.id)
        return driver.RunQuery(query)

    def GetSimilarRecipes(self):
        query = '''
        MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)<-[:CONTAINS]-(rec:Recipe)
        WHERE r.id = {}
        WITH rec, COUNT(*) as commonIngredients
        RETURN  rec.id AS id, rec.title AS title, rec.description AS description, rec.skill_level AS skill_level, rec.ratings AS ratings, toInteger(rec.cooking_time)/60 as cooking_time, toInteger(rec.prep_time)/60 as prep_time, rec.servings as servings
        ORDER BY commonIngredients
        LIMIT 20
        '''.format(self.id)
        return driver.RunQuery(query)

    def AddRating(self):
        query = '''
        MATCH (r:Recipe)
        WHERE r.id = {}
        SET r.ratings = r.ratings +1
        '''.format(self.id)
        driver.RunQuery(query)

    def UserLikesRecipe(self,username):
        query = '''
        MATCH (r:Recipe)<-[l:LIKES]-(u:User)
        WHERE r.id = {} AND u.username = '{}'
        RETURN COUNT(l) > 0 AS user_likes
        '''.format(self.id,username)
        return driver.RunQuery(query)

    def UserSavedRecipe(self,username):
        query = '''
        MATCH (r:Recipe)<-[s:SAVED]-(u:User)
        WHERE r.id = {} AND u.username = '{}'
        RETURN COUNT(s) > 0 as user_saved
        '''.format(self.id,username)
        # return True
        return driver.RunQuery(query)



class Ingredient(object):
    """docstring for Ingredient"""
    def __init__(self, name):
        self.name = name

    def IsIngredient(self):
        query='''
        MATCH (i:Ingredient)
        WHERE i.name = '{}'
        RETURN count(i) > 0 AS exists
        '''.format(self.name)
        return driver.RunQuery(query)

    def GetIngredientByName(self):
        query = '''
        MATCH (i:Ingredient)
        WHERE i.name = '{}'
        RETURN i.name AS name
        '''.format(self.name)
        return driver.RunQuery(query)

    def GetRecipesByIngredient(self):
        query = '''
        MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
        WHERE i.name = '{}'
        RETURN r.id as id, r.title AS title, r.description AS description, r.skill_level AS skill_level, r.ratings AS ratings, toInteger(r.cooking_time)/60 as cooking_time, toInteger(r.prep_time)/60 as prep_time, r.servings as servings
        '''.format(self.name)
        return driver.RunQuery(query)


class Collection(object):
    def __init__(self, name):
        self.name = name

    def IsCollection(self):
        query='''
        MATCH (c:collection)
        WHERE c.name = '{}'
        RETURN count(c) > 0 AS exists
        '''.format(self.name)
        return driver.RunQuery(query)

    def GetCollectionByName(self):
        query = '''
        MATCH (c:Collection)
        WHERE c.name = '{}'
        RETURN c.name AS name
        '''.format(self.name)
        return driver.RunQuery(query)

    def GetRecipesByCollection(self):
        query = '''
        MATCH (r:Recipe)-[:ORGANIZEDINTO]->(c:Collection)
        WHERE c.name = '{}'
        RETURN r.id as id, r.title AS title, r.description AS description, r.skill_level AS skill_level, r.ratings AS ratings, toInteger(r.cooking_time)/60 as cooking_time, toInteger(r.prep_time)/60 as prep_time, r.servings as servings
        '''.format(self.name)
        return driver.RunQuery(query)

        






        