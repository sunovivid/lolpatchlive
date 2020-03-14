from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(VersionModel)
admin.site.register(HeaderModel)
admin.site.register(ArticleModel)
admin.site.register(MinorUpdateModel)
admin.site.register(MinorUpdateItemModel)
admin.site.register(ChampionPatchModel)
admin.site.register(ChampionMinorPatchModel)
