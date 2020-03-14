from django.shortcuts import render
from django.shortcuts import *
import versions
# Create your views here.

from .models import *
from django.core.exceptions import ObjectDoesNotExist

sampleData = {
    "prev": {
        "version": 10.4,
        "summary": "",
        "hotfix": "Hotfix 2 티아맷/굶주린 히드라 버그 수정",
        "tags": ["정글 챔피언", "상단 공격로의 중요성"],
        "champions": ["알리스타","카이사"]
    },
    "now": {

    },
    "next": None
}

def index(request):
    vModels = VersionModel.objects.all().order_by('updateDate')
    versionModelDict = {}
    context = {}

    # for i, v in enumerate(vModels):
    #     if str(v.version) == versions.getLiveClientVersion():
    #         versionModelDict["now"] = vModels[i]
    #         versionModelDict["prev"] = vModels[i-1] if i-1 > 0 else None
    #         versionModelDict["next"] = vModels[i+1] if i+1 < len(vModels) else None
    #         break
    # for key, versionModel in versionModelDict.items():
    #     if versionModel is not None:
    #         context[key]["version"] = versionModel.version
    #         context[key]["summary"] = versionModel.summary
    #         minorUpdate = get_list_or_404(MinorUpdateModel, version=versionModel)[0]
    #         context[key]["hotfix"] = "Hotfix #{} ".format(len(minorUpdate)) + minorUpdate.updateTitle
    #         headerModels = get_list_or_404(HeaderModel, version=VersionModel)
    #         context[key]["tags"] = list(map(lambda x: x.header, headerModels))
    #         context[key]["champions"] = list(map(lambda x: x.championName, get_list_or_404(ChampionPatchModel, version=versionModel)))
    return render(request, 'updates/index.html', {"version":vModels[0].version})
# Create your views here.

