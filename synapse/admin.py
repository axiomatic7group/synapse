from django.contrib import admin
from django.apps import apps
from .models import *

for x_model in apps.get_models():
    try:
        admin.site.register(x_model)
    except:
        #print("model " + str(x_model) + " not loaded.")
        pass