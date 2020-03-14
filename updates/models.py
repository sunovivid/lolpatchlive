from django.db import models
from django.utils import timezone

DISPLAY_CHARNUM = 10
def clip(string):
    string = str(string)
    if len(string) > DISPLAY_CHARNUM:
        return str(string)[:DISPLAY_CHARNUM]+"..."
    return string

class VersionModel(models.Model):
    version = models.CharField(max_length=6)
    summary = models.TextField(default="")
    updateDate = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ['version']

    def __str__(self):
        return str(self.version)

class HeaderModel(models.Model):
    header = models.CharField(max_length=255)
    version = models.ForeignKey(VersionModel, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.version.version) + ' #' + str(self.header)

class ArticleModel(models.Model):
    contentHtml = models.TextField()
    header = models.ForeignKey(HeaderModel, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.header.version.version) + '/ ' + str(self.header.header) + '/ ' + clip(self.contentHtml)

class MinorUpdateModel(models.Model):
    updateTitle = models.CharField(primary_key=True, max_length=255, default="아직 추가 패치 노트 없음")
    version = models.ForeignKey(VersionModel, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.updateTitle)

class MinorUpdateItemModel(models.Model):
    itemName = models.CharField(max_length=255)
    item = models.TextField()
    minorUpdate = models.ForeignKey(MinorUpdateModel, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.itemName)

class ChampionPatchModel(models.Model):
    championName = models.CharField(max_length=255, default="")
    contentHtml = models.TextField(default="")
    championSummaryText = models.TextField(default='')
    championQuoteText = models.TextField(default='')
    version = models.ForeignKey(VersionModel, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.championName) + "[{}]".format(self.version.version) + ': ' + clip(self.championSummaryText)

class ChampionMinorPatchModel(models.Model):
    championName = models.CharField(max_length=255, default="")
    contentHtmlList = models.TextField(default="")
    minorUpdate = models.ForeignKey(MinorUpdateModel, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.championName) + "[{}]".format(self.minorUpdate.version.version,self.minorUpdate.updateTitle) + ': ' + clip(self.contentHtmlList)