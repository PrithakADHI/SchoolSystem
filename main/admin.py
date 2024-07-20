from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Semester)
admin.site.register(models.Subject)
admin.site.register(models.Material)
admin.site.register(models.Chapter)
admin.site.register(models.Syllabus)
admin.site.register(models.UserRole)
admin.site.register(models.Assignment)
admin.site.register(models.AssignmentAnswer)
admin.site.register(models.Sgpa)