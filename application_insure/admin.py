from django.contrib import admin
from .models import ContactUs, SearchRecord

# Register your models here.
#admin.site.register(ContactUs)

admin.site.site_header = 'BimaMitra Admin'                    # default: "Django Administration"
admin.site.index_title = 'Features area'                 # default: "Site administration"
admin.site.site_title = 'BimaMitra'                      # default: "Django site admin"


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name','email', 'subject', 'message']

@admin.register(SearchRecord)
class searchAdmin(admin.ModelAdmin):
    list_display = ['date_time','username','user_input']