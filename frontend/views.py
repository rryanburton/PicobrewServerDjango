import os

from os import path

from django.shortcuts import render, redirect
from werkzeug.utils import secure_filename
from beerxml.picobrew_parser import PicoBrewParser as BeerXMLParser
from functools import reduce


FILE_EXTENSIONS = ["xml", "beerxml"]


# -------- Routes --------
def index(request):
    return render(request, "index.html")


def get_recipes(recipe_path="recipes"):

    files = list(filter(filter_by_extensions, os.listdir("recipes")))
    files = [os.path.join(recipe_path, filename) for filename in files]

    recipes = [get_recipe(file) for file in files]
    recipes = reduce(lambda x, y: x+y, recipes)  # flatten dat shit
    print("recipes: {}".format(recipes))

    return recipes


def get_recipe(file):

    parser = BeerXMLParser()
    return parser.parse(file)


def recipes(request):
    print("in recipes")
    return render(request, "recipes.html", {'recipes': get_recipes()})


def handle_uploaded_file(file, filename):
    with open(filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


# @frontend.route("/upload", methods=["POST"])
def upload_recipe(request):

    def isAllowed(filename):
        return len(filter_by_extensions(filename)) > 0

    redirect_url = "index"
    print("request: {}".format(request.FILES.getlist("recipes")))
    for file in request.FILES.getlist("recipes"):
        print("file: {}".format(file.name))
        if isAllowed(file.name):
            filename = path.join("recipes", secure_filename(file.name))
            print("filename: {}".format(filename))

            # file.save(filename)
            handle_uploaded_file(file, filename)
            redirect_url = "validate"
            request.session["recipe_file"] = filename
        else:
            print("Invalid BeerXML file <%s>." % file.filename)

    return redirect(redirect_url)



# @frontend.route("/validate")
def validate(request):

    file = request.session["recipe_file"]
    print("file: {}".format(file))
    recipe = get_recipe(file)[0]
    print("recipe: {}".format(recipe))
    return render(request, "validate.html", {'recipe': recipe})

# @frontend.route("/validate_recipe", methods=["POST"])
def validate_recipe(request):

    redirect_url = "recipes"
    form_data = request.form

    if not form_data.getlist("accept_eula") or form_data.getlist("action") == "cancel":
        file = request.session["recipe_file"]
        os.remove(file)
        redirect_url = "index"

    return redirect(redirect_url)


# -------- Utility --------
def filter_by_extensions(filename):
    return [ext for ext in ["xml", "beerxml"] if ext in filename]

