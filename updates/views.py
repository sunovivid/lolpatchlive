import re
from django.shortcuts import render
from django.shortcuts import *

import tools
# Create your views here.

from .models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

sampleData = {
    "prev": {
        "version": 10.4,
        "summary": "",
        "hotfix": "Hotfix 2 티아맷/굶주린 히드라 버그 수정",
        "tags": ["정글 챔피언", "상단 공격로의 중요성"],
        "champions": { #챔피언 이름:image url
            "킨드레드":"https://am-a.akamaihd.net/image?f=http://ddragon.leagueoflegends.com/cdn/10.5.1/img/champion/Kindred.png",
            "카이사":""
        }
    },
    "now": {

    },
    "next": None
}

def index(request):
    vModels = VersionModel.objects.all().order_by('updateDate')
    versionModelDict = {}
    context = {
        "prev":{},
        "now":{},
        "next":{}
    }

    for i, v in enumerate(vModels):
        if str(v.version) == tools.getLiveClientVersion():
            versionModelDict["now"] = vModels[i]
            versionModelDict["prev"] = vModels[i-1] if i-1 > 0 else None
            versionModelDict["next"] = vModels[i+1] if i+1 < len(vModels) else None
            break
    for key, versionModel in versionModelDict.items():
        if versionModel is not None:
            context[key]["version"] = versionModel.version
            context[key]["summary"] = versionModel.summary
            minorUpdateModels = MinorUpdateModel.objects.filter(version=versionModel).order_by('-updateDate')
            if len(minorUpdateModels) <= 1:
                hotfixText = ''
            else:
                hotfixText = "Hotfix #{} ".format(len(minorUpdateModels)-1) + minorUpdateModels[1].updateTitle if not '아직 추가 패치 노트 없음' in minorUpdateModels[1].updateTitle else ''
            context[key]["hotfix"] = hotfixText
            headerModels = HeaderModel.objects.filter(version=versionModel).order_by('-updateDate')
            context[key]["tags"] = list(map(lambda x: x.header, headerModels))
            context[key]["champions"] = list(map(lambda x: (x.championName, tools.getChampionImageUrl(x.championName)), get_list_or_404(ChampionPatchModel, version=versionModel)))
    return render(request, 'updates/index.html', context)

def champion(request, name) :

    def removeTag(tag, html):
        p = re.compile("<{}.*>.*</{}>".format(tag, tag))
        m = p.search(html)
        if m is not None:
            html = html[:m.start()] + html[m.end():]
        return html


    updates = ChampionPatchModel.objects.filter(championName=name).order_by('-updateDate')
    championPatchNoteList = list(map(lambda update:(update.version, removeTag("h3",removeTag("a",update.contentHtml))), updates))

    return render(request, 'updates/champion.html', {"updates":championPatchNoteList})