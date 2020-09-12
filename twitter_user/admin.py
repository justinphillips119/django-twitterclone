from django.contrib import admin
from twitter_user.models import TwitterUser
from twitter_user.forms import TwitterUserForm
from django.contrib.auth.admin import UserAdmin


class TwitterUserAdmin(UserAdmin):
    model = TwitterUser
    add_form = TwitterUserForm

    fieldsets = (
        *UserAdmin.fieldsets, (
            'User Information', {
                'fields': (
                    'display_name',
                    'bio',
                    'following'
                )
            }
        )
    )

admin.site.register(TwitterUser, TwitterUserAdmin)
