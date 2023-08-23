from django.contrib import admin

# Register your models here.

from account.models import Account
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_predseda', 'is_organizator', 'is_clen', 'is_neregistrovany', 'first_name', 'second_name', 'index', 'si_number')
    search_fields = ('email', 'username', 'first_name', 'second_name')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)