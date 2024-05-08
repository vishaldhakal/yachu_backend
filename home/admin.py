from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import SiteConfiguration, FAQCategory, FAQ, Department, TeamMember, Testimonial, ImageGallery, VideoGallery,Banners,Product, FormData,Member,FileSchema
from unfold.admin import ModelAdmin


class SiteConfigurationAdmin(SingletonModelAdmin,ModelAdmin):
    pass

admin.site.register(SiteConfiguration,SiteConfigurationAdmin)

admin.site.register(FAQCategory,ModelAdmin)
admin.site.register(FAQ,ModelAdmin)
admin.site.register(Department,ModelAdmin)
admin.site.register(TeamMember,ModelAdmin)
admin.site.register(Testimonial,ModelAdmin)
admin.site.register(ImageGallery,ModelAdmin)
admin.site.register(VideoGallery,ModelAdmin)
admin.site.register(Banners,ModelAdmin)
admin.site.register(Product,ModelAdmin)
""" admin.site.register(FormData)
admin.site.register(Member)
admin.site.register(FileSchema) """