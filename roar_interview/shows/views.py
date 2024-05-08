from django.http import JsonResponse, HttpResponseNotFound
from .models import Shows, ShowInfos, ShowUnitRoles 
from datetime import datetime

def shows(request):
    if request.method == 'GET':
        queryStringUid = request.GET.get('UID')
        # 1. Check input
        if(queryStringUid is None):
            # 2. Select all show from Shows
            
            # Query all shows with related information
            showQuerySet = Shows.objects.all().prefetch_related('showinfos_set', 'showunitroles_set')
        else:
            # 2. Select show from Shows with UID.
            showQuerySet = Shows.objects.filter(UID=queryStringUid).prefetch_related('showinfos_set', 'showunitroles_set')
            
        # Declare reconstructedShowList to store shows
        reconstructedShowList = []
        unitTypeList = ['masterUnit', 'subUnit', 'supportUnit', 'otherUnit']
        # Iterate through the deserialized data to include related objects
        for show in showQuerySet:
            reconstructedShow = {}
            reconstructedShow['version'] = show.Version
            reconstructedShow['UID'] = show.UID
            reconstructedShow['title'] = show.Title
            reconstructedShow['category'] = show.Category

            # Retrieve related show info
            showInfoQuerySet = ShowInfos.objects.filter(ShowID=show.ShowID)
            reconstructedShow['showInfo'] = [{'time': showInfoQuery.Time if type(showInfoQuery.Time) != datetime else showInfoQuery.Time.strftime('%Y/%m/%d %H:%M:%S'), 'location': showInfoQuery.LocationID.Address, 'locationName': showInfoQuery.LocationID.Name,'onSales': showInfoQuery.OnSales, 'price': showInfoQuery.Price, 'latitude': showInfoQuery.LocationID.Latitude, 'longitude': showInfoQuery.LocationID.Longitude, 'endTime': showInfoQuery.EndTime if type(showInfoQuery.EndTime) != datetime else showInfoQuery.EndTime.strftime('%Y/%m/%d %H:%M:%S')} for showInfoQuery in showInfoQuerySet]

            reconstructedShow['showUnit'] = show.ShowUnit
            reconstructedShow['discountInfo'] = show.DiscountInfo
            reconstructedShow['descriptionFilterHtml'] = show.DescriptionFilterHtml
            reconstructedShow['imageUrl'] = show.ImageUrl

            # Retrieve related unit roles
            for unitType in unitTypeList:
                showUnitRoleQuerySet = ShowUnitRoles.objects.filter(ShowID=show.ShowID, Role=unitType)
                reconstructedShow[unitType] = [showUnitRoleQuery.UnitID.Name for showUnitRoleQuery in showUnitRoleQuerySet]

            reconstructedShow['webSales'] = show.WebSales
            reconstructedShow['sourceWebPromote'] = show.SourceWebPromote
            reconstructedShow['comment'] = show.Comment
            reconstructedShow['editModifyDate'] = show.EditModifyDate if type(show.EditModifyDate) != datetime else show.EditModifyDate.strftime('%Y/%m/%d %H:%M:%S')
            reconstructedShow['sourceWebName'] = show.SourceWebName
            reconstructedShow['startDate'] = show.StartDate if type(show.StartDate) != datetime else show.StartDate.strftime('%Y/%m/%d')
            reconstructedShow['endDate'] = show.EndDate if type(show.EndDate) != datetime else show.StartDate.strftime('%Y/%m/%d')
            reconstructedShow['hitRate'] = show.HitRate

            # Append the show data to the reconstructed data list
            reconstructedShowList.append(reconstructedShow)

        return JsonResponse(reconstructedShowList, safe=False, json_dumps_params={'ensure_ascii': False, 'separators': (',', ':')})
    return HttpResponseNotFound()