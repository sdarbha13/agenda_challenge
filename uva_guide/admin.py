from django.contrib import admin
from uva_guide.models import Event

from .models import Profile, Org, OrgType
# Register your models here.

admin.site.register(Event)



class OrgTypeInline(admin.StackedInline):
    model = Org.type.through
    extra = 0
#     model = Org

class OrgAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', )
    list_filter = ['name']
    search_fields = ['name']
    # fieldsets = [
    #     (None, {'fields':['name', 'description', ]}),
    # ]
    inlines = [OrgTypeInline,]
    filter_horizontal = ('type',) 

class OrgTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ['name']
    search_fields = ['name']
    # fieldsets = [
    #     (None, {'fields':['name', 'description', ]}),
    # ]
    # inlines = [OrgTypeInline,]

admin.site.register(Org, OrgAdmin)
admin.site.register(OrgType, OrgTypeAdmin)

