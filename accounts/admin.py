from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'name', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'name')
    ordering = ('email',)


admin.site.register(Walker)
admin.site.register(Wanderer)
admin.site.register(WandererPreferences)
admin.site.register(Language)
admin.site.register(WalkingPace)
admin.site.register(Charity)
admin.site.register(User, UserAdmin)