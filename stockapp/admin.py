from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'account_type', 'balance')  # Fields to display in the list view
    list_filter = ('account_type',)  # Add filters on the right side
    search_fields = ('user__username', 'account_type')  # Enable search functionality
    raw_id_fields = ('user',)  # Add a search lookup for the user field

    # Optional: group fields in the detail view
    fieldsets = (
        (None, {
            'fields': ('user', 'account_number')
        }),
        ('Financial Information', {
            'fields': ('balance',)
        }),
    )
