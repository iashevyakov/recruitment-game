from django.contrib import admin

# Register your models here.
from recruiting.models import Planet, Sith, Test, Question

admin.site.register(Planet)
admin.site.register(Sith)
admin.site.register(Test)
admin.site.register(Question)
