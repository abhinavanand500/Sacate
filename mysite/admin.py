from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Contact)
admin.site.register(Userinfo)
admin.site.register(DonatedFood)
admin.site.register(DonatedCloth)
admin.site.register(NewsFeed)
admin.site.register(Notification)
admin.site.register(DonatedOther)