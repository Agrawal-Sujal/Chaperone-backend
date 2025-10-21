from django.contrib import admin
from rest_framework.authtoken.models import Token

class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    search_fields = ('user__email',)
    readonly_fields = ('key', 'created')

admin.site.register(Token, TokenAdmin)
