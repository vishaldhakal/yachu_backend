from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import SiteConfiguration, FAQCategory, FAQ, Department, TeamMember, Testimonial, ImageGallery, VideoGallery,Banners,Product

admin.site.register(SiteConfiguration, SingletonModelAdmin)
admin.site.register(FAQCategory)
admin.site.register(FAQ)
admin.site.register(Department)
admin.site.register(TeamMember)
admin.site.register(Testimonial)
admin.site.register(ImageGallery)
admin.site.register(VideoGallery)
admin.site.register(Banners)
admin.site.register(Product)