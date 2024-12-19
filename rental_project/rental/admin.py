from django.contrib import admin

from .models import Team, Personnel, Part, Aircraft

# Register your models here.

admin.site.register(Team)
admin.site.register(Personnel)
admin.site.register(Part)
admin.site.register(Aircraft)