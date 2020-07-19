from django.contrib import admin
from .models import Cat, Ad, Sub, Pic, Tag, TagLink


class CatAdmin(admin.ModelAdmin):
    list_display = ('cat', 'logo', 'id')


class PicAdmin(admin.ModelAdmin):
    list_display = ('url', 'ad_id')


class AdAdmin(admin.ModelAdmin):

    list_display = (
        'title', 'description', 'price', 'phone_number', 'id',
        'user_id', 'url', 'date')


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'id')


class SubAdmin(admin.ModelAdmin):
    list_display = ('sub',)


class TagLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag_id', 'sub_id')


admin.site.register(TagLink, TagLinkAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Pic, PicAdmin)
admin.site.register(Sub, SubAdmin)
admin.site.register(Cat, CatAdmin)
admin.site.register(Ad, AdAdmin)

# Register your models here.
