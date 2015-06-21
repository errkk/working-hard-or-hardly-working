from django.contrib import admin

from .models import Token

class TokenAdmin(admin.ModelAdmin):
    readonly_fields = ('modified', )
    list_display = ('user', 'access_token', 'expires', )
    list_filter = ('expires', 'modified', )

admin.site.register(Token, TokenAdmin)
