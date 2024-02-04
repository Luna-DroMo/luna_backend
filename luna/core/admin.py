from django.contrib import admin
from .models import User
from .models import Module
from .models import StudentUser
from .models import StudentModule
from .models import Form

admin.site.register(User)
admin.site.register(Module)
admin.site.register(StudentUser)
admin.site.register(StudentModule)
admin.site.register(Form)
