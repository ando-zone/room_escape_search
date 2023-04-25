from django.contrib import admin
from .models import Branch

# Register your models here.
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "address",
    ]
    list_filter = [
        "name",
        "city",
        "district"
    ]
    search_fields = [
        "name__startswith",
    ]
