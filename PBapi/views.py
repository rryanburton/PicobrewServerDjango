import json
import os
# from webargs import fields
import re

import time
import uuid

from webargs.djangoparser import use_args, DjangoParser, use_kwargs
from marshmallow import fields
from django.shortcuts import render
from django.http import HttpResponse

SYSTEM_USER = "00000000000000000000000000000000"
arg_parser = DjangoParser()
SESSION_PATH = 'nothing'

machine_args = {
    "user": fields.Str(required=True),
    "machine": fields.Str(required=True),
}


@use_args(machine_args)
def parse_recipe_request(request, args):
    user = args['user']
    machine = args['machine']
    print("user: {}, machine: {}".format(user, machine))
    if user == SYSTEM_USER:
        return get_cleaning_recipes()
    else:
        if machine:
            return get_picobrew_recipes()

    # default response
    return "\r\n##"
    # return HttpResponse('')


@use_args(machine_args)
def check_sync(user):
    return "\r\n#!#"


def get_cleaning_recipes():
    return "#Cleaning v1/7f489e3740f848519558c41a036fe2cb/Heat Water,152,0,0,0/Clean Mash,152,15,1,5/Heat to Temp,152,0,0,0/Adjunct,152,3,2,1/Adjunct,152,2,3,1/Adjunct,152,2,4,1/Adjunct,152,2,5,1/Heat to Temp,207,0,0,0/Clean Mash,207,10,1,0/Clean Mash,207,2,1,0/Clean Adjunct,207,2,2,0/Chill,120,10,0,2/|Rinse v3/0160275741134b148eff90acdd5e462f/Rinse,0,2,0,5/|#"


def get_picobrew_recipes():
    all_recipes = get_recipes()
    filtered_recipes = filter(lambda recipe: recipe.steps, all_recipes)
    recipes = map(lambda recipe: recipe.serialize(), filtered_recipes)
    recipes = "|".join(recipes)

    return "#{0}|#".format(recipes)
#
#
# # ----------- SESSION LOGGING -----------
# def parse_session_request(session, recipe):
#     if recipe:
#         args = arg_parser.parse({"user": Arg(str), "firm": Arg(str), "machine": Arg(str)})
#         return create_new_session(recipe, args)
#
#     if session:
#         args = arg_parser.parse({"data": Arg(str), "state": Arg(str), "step": Arg(str), "code": Arg(int)})
#         return log_to_session(session, args)
#
#     # default fallthrough
#     abort()
#
#
# def create_new_session(recipe_id, args):
#     session_id = uuid.uuid4().hex[:32]
#     session_file = "{0}.json".format(session_id)
#
#     recipe_file = None
#
#     for recipe in get_recipes():
#         if recipe.id == recipe_id:
#             recipe_file = recipe.filename
#
#     session_data = {
#         "date": time.strftime("%x"),
#         "recipe_id": recipe_id,
#         "recipe_filename": recipe_file,
#         "session_id": session_id,
#         "steps": []
#     }
#
#     try:
#         with open(os.path.join(SESSION_PATH, session_file), 'w') as out_file:
#             json.dump(session_data, out_file)
#
#     except IOError:
#         return "##"
#
#     return "#{0}#".format(session_id)
#
#
# def log_to_session(session_id, args):
#     session_file = "{0}.json".format(session_id)
#     data = args["data"]
#     code = args["code"]
#     machine_state = args["step"]
#
#     try:
#         if not os.path.exists(SESSION_PATH):
#             os.mkdir(SESSION_PATH)
#
#         with open(os.path.join(SESSION_PATH, session_file), 'r') as in_file:
#             session = json.load(in_file)
#
#             if code == 1:
#                 # new program step e.g. "Heating"
#
#                 session_step = {
#                     "name": data,
#                     "temperatures": {}
#                 }
#                 session["steps"].append(session_step)
#
#             elif code == 2:
#                 # temperature data for current step
#
#                 temps = re.findall(r"/([0-9]+)", data)
#                 current_time = time.strftime("%X")
#
#                 session_step = session["steps"][-1]
#                 session_step["temperatures"][current_time] = temps
#
#                 session["machine_state"] = machine_state
#
#             elif code == 3:
#                 # end session
#
#                 session["steps"].append({"name": "Session Ended"})
#
#         with open(os.path.join(SESSION_PATH, session_file), 'w') as out_file:
#             json.dump(session, out_file)
#
#     except IOError:
#         pass
#
#     return ""
