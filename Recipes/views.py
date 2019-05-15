from .models import User, Recipe, Ingredient, Collection

from flask import Flask, request, session, redirect, url_for, render_template, flash, abort,g,jsonify

from functools import wraps
import json

# Application Definition
# ___________________________________________________________________________________________

app = Flask(__name__)



# Error Handling
# ___________________________________________________________________________________________
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

@app.errorhandler(400)
def handle_bad_request(e):
    return 'You made a very bad request!', 400

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers['session'] is None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



# Home
# ___________________________________________________________________________________________
@app.route('/')
def index():
    return render_template('index.html')


# Recipes
# ___________________________________________________________________________________________
@app.route('/recipes', methods=['GET', 'POST'])
# @login_required
def view_recipes():
    if request.method == 'GET':
        return render_template('recipes.html')
    elif request.method == 'POST':
        selected_option = request.form["start_option"]
        if selected_option == "Ingredient":
            search_query = request.form['build_option'].split(",")
            # flash(search_query)
            recipes = Recipe.GetRecipesByIngredients(search_query)
            return render_template('recipes.html', recipes=recipes)
        elif selected_option == "Collection":
            search_query = request.form['search_option']
            if Collection(search_query).IsCollection():
                recipes = Collection(search_query).GetRecipesByCollection()
                return render_template('recipes.html', recipes=recipes)
        elif selected_option == "Keyword":
            search_query = request.form['search_option']
            recipes = Recipe.GetRecipesByKeyword(search_query)
            return render_template('recipes.html', recipes=recipes)
        elif selected_option == "Total_Time":
            search_query = request.form['cat_option']
            gt = 0
            if search_query == 15:
                gt = 0
            elif search_query == 30:
                gt = 15
            elif search_query == 60:
                gt = 30
            elif search_query == 60:
                gt = 60
            recipes = Recipe.GetRecipesByTotalTime(search_query,gt)
            return render_template('recipes.html', recipes=recipes)
        elif selected_option == "Skill_Level":
            search_query = request.form['cat_option']
            recipes = Recipe.GetRecipesBySkill(search_query)
            return render_template('recipes.html', recipes=recipes)
        elif selected_option == "Rating":
            search_query = request.form['cat_option']
            if search_query == "Liked":
                recipes = Recipe.GetRecipesByTopRating()
            elif search_query == "Saved":
                recipes = Recipe.GetRecipesByTopSaved()
            return render_template('recipes.html', recipes=recipes)
    else:
        return render_template('index.html')

@app.route('/recipes/<recipe_id>', methods=['GET', 'POST'])
def view_recipe_detail(recipe_id):
    if request.method == 'GET':
        username = session.get('username')
        if Recipe(recipe_id).IsRecipe().single()['exists']:
            recipe = Recipe(recipe_id).GetRecipeByID()
            ingredients = Recipe(recipe_id).GetIngredientsByRecipe()
            collections = Recipe(recipe_id).GetCollectionsByRecipe()
            created_date = Recipe(recipe_id).GetCreatedDate()
            keywords = Recipe(recipe_id).GetKeywordsByRecipe()
            courses = Recipe(recipe_id).GetCoursesByRecipe()
            author = Recipe(recipe_id).GetAuthorByRecipe()
            skill_level = Recipe(recipe_id).GetSkillByRecipe()
            diet_types = Recipe(recipe_id).GetDietByRecipe()
            nutrition = Recipe(recipe_id).GetNutritionByRecipe()
            user_likes = Recipe(recipe_id).UserLikesRecipe(username)
            user_saved = Recipe(recipe_id).UserSavedRecipe(username)
            return render_template(
                'recipe.html', 
                recipe=recipe,
                ingredients=ingredients,
                collections=collections,
                created_date=created_date,
                keywords=keywords,
                courses=courses,
                author=author,
                skill_level=skill_level,
                diet_types=diet_types,
                nutrition = nutrition,
                user_likes=user_likes,
                user_saved=user_saved)
        else:
            redirect(url_for('index'))
    elif request.method == 'POST':
        value = request.form['recipe']
        return render_template('recipe.html')


@app.route('/recipes/<recipe_id>/<link>', methods=['GET'])
def view_recipe_link(recipe_id,link):
    # flash(link)
    referer = request.headers['Referer']
    if referer[:30] == "http://127.0.0.1:5000/recipes/":
        search_query = int(referer[30:])

    if link == "similar":
        recipes = Recipe(search_query).GetSimilarRecipes()
    return render_template('recipes.html', recipes=recipes,page="similar")


@app.route('/submit/', methods=['POST'])
def submit():
    if request.method == 'POST':
        if request.is_json:

            data = json.loads(request.data)

            button = data.get("button")
            recipe_id = data.get("recipe")
            user_id = data.get("user")

            response = {}
            if button == "like":
                # flash(user_id,recipe_id)
                Recipe(recipe_id).AddRating()
                User(user_id).LikeRecipe(recipe_id)
                value =  "Liked recipe"
                response['button'] = "like"
                response['likes'] = Recipe(recipe_id).GetLike().single()['ratings']
            elif button == "save":
                User(user_id).SaveRecipe(recipe_id)
                value =  "Added Recipe"
                response['button'] = "save"
            elif button == "remove":
                User(user_id).RemoveRecipe(recipe_id)
                value =  "Removed Recipe"
                response['button'] = "remove"
            else:
                value = "oops"
                response['button'] = "oops"
            return jsonify(response)
        else:
            return "No"



# Ingredients
# ___________________________________________________________________________________________
@app.route('/ingredients')
def view_ingredients():
    return render_template('ingredients.html') 

@app.route('/ingredients/<ingredient_name>')
def view_ingredient_detail(ingredient_name):
    if Ingredient(ingredient_name).IsIngredient().single()['exists']:
        ingredient = Ingredient(ingredient_name).GetIngredientByName()
        return render_template('ingredient.html', ingredient=ingredient) 
    else:
        redirect(url_for('index'))


@app.route('/collections')
def view_collections():
    return render_template('collections.html') 

@app.route('/collections/<collection_name>')
def view_collection_detail(collection_name):
    if Collection(collection_name).IsCollection().single()['exists']:
        collection = Collection(collection_name).GetCollectionByName()
        return render_template('collection.html', collection=collection)
    else:
        redirect(url_for('index'))



# User
# ___________________________________________________________________________________________
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) < 1:
            flash('Your username must be at least one character.')
        elif len(password) < 5:
            flash('Your password must be at least 5 characters.')
        elif not User(username).register(password):
            flash('Hello '+username)
            flash('A user with that username already exists.')
        else:
            session['username'] = username
            return redirect(url_for('view_recipes'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not User(username).verify_password(password):
            flash('Invalid login.')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('view_recipes'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))

@app.route('/profile/<username>', methods=['GET','POST'])
# @login_required
def profile(username):
    # flash(request.headers)
    recipes = User(username).GetSaved()
    return render_template('recipes.html',username=username, recipes=recipes,page="profile")
