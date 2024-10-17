from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from badmotoboy.users.models import UserProfile, Gender
from badmotoboy.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email", "latitude", "longitude")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
    inlines = [UserProfileInline]


class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain')

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)
admin.site.register(Gender)
