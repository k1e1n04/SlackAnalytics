from curses.ascii import EM
from django.contrib import admin

# Register your models here.
from analytics.models import Base,Department,Channel,Employee,Post
admin.site.register(Base)
admin.site.register(Department)
admin.site.register(Channel)
admin.site.register(Employee)
admin.site.register(Post)