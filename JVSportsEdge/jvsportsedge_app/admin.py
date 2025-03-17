from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Team, Player, Payment

# Customizing the User Adminclass CustomUserAdmin(UserAdmin):
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'get_role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

    def get_role(self, obj):
        return obj.get_role_display()
    get_role.admin_order_field = 'role'
    get_role.short_description = 'Role'

    
# Registering Models
admin.site.register(Payment)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(CustomUser, CustomUserAdmin)



