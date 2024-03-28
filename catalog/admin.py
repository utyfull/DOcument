from django.contrib import admin

from .models import AuthTable, OwnDocTable, ForeignDocTable, StatusTable, CommentTable

from .models import Book


# Register your models here.


@admin.register(AuthTable)
class AuthAdmin(admin.ModelAdmin):
    list_display = ('username', 'pssword', 'reg_time')
    list_filter = ('username', 'reg_time')
        
# Register the Admin classes for BookInstance using the decorator

@admin.register(Book)
class Book(admin.ModelAdmin):
    pass

@admin.register(OwnDocTable)
class OwnDocAdmin(admin.ModelAdmin):
    pass

@admin.register(ForeignDocTable)
class ForeignDocAdmin(admin.ModelAdmin):
    pass

@admin.register(StatusTable)
class StatusAdmin(admin.ModelAdmin):
    pass

@admin.register(CommentTable)
class CommentAdmin(admin.ModelAdmin):
    pass



