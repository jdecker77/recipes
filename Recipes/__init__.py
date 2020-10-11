from .views import recipes
import os
recipes.secret_key = os.urandom(24)