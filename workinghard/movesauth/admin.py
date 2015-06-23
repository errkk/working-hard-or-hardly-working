from django.contrib import admin

from .models import Token, UserData


class TokenAdmin(admin.ModelAdmin):
    readonly_fields = ('modified', )
    list_display = ('user', 'access_token', 'expires', )
    list_filter = ('expires', 'modified', )


class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'workplace_name', )


admin.site.register(Token, TokenAdmin)
admin.site.register(UserData, UserDataAdmin)
