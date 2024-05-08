# Import json to convert shows data in .json file.
import json
from shows.models import Shows, Locations, ShowInfos ,Units, ShowUnitRoles
# Import datetime to convert time(YYYY-MM-DD HH:MM:ss) from shows data to correct format(YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ])
from datetime import datetime


# Parse the JSON file from shows-data.json
with open('/Users/wangyouhao/Desktop/roar-interview/roar_interview/shows_data.json', 'r') as shows:
    showList = json.load(shows)

# declare list for iterate through units
unitTypeList = ['masterUnit', 'subUnit', 'supportUnit', 'otherUnit']

# Convert JSON data to Django model instances and save to the database
for show in showList:
    # Insert show into Shows
    showInstance = Shows(
        Version = show['version'],
        UID = show['UID'],
        Title = show['title'], 
        Category = show['category'], 
        ShowUnit = show['showUnit'], 
        DiscountInfo = show['discountInfo'], 
        DescriptionFilterHtml = show['descriptionFilterHtml'], 
        ImageUrl = show['imageUrl'], 
        WebSales = show['webSales'], 
        SourceWebPromote = show['sourceWebPromote'], 
        Comment = show['comment'], 
        EditModifyDate = None if show['editModifyDate'] == '' else datetime.strptime(show['editModifyDate'], '%Y/%m/%d %H:%M:%S'), 
        SourceWebName = show['sourceWebName'],
        StartDate = None if show['startDate'] == '' else datetime.strptime(show['startDate'], '%Y/%m/%d').date(),
        EndDate = None if show['endDate'] == '' else datetime.strptime(show['endDate'], '%Y/%m/%d').date(), 
        HitRate = show['hitRate']
        # Add other fields as needed
    )
    showInstance.save()
    
    # Insert showInfo
    for info in show['showInfo']:
        # Insert unique location into Locations
        if(Locations.objects.filter(Address = info['location']).first() is None):
            locationInstance = Locations(
                Address = info['location'],
                Name = info['locationName'],
                Latitude = info['latitude'], 
                Longitude = info['longitude']
            )
            locationInstance.save()
            
        # Insert showInfo and LocationID into ShowInfos
        showInfoInstance = ShowInfos(
            ShowID = showInstance,
            Time = None if info['time'] == '' else datetime.strptime(info['time'], '%Y/%m/%d %H:%M:%S'), 
            LocationID = Locations.objects.filter(Address = info['location']).first(), 
            OnSales = info['onSales'], 
            Price = info['price'], 
            EndTime = None if info['endTime'] == '' else datetime.strptime(info['endTime'], '%Y/%m/%d %H:%M:%S')
        )
        showInfoInstance.save()
    # Insert masterUnit, subUnit, supportUnit and otherUnit into Units
    for unitType in unitTypeList:
        for unit in show[unitType]:
            # Insert unique unit into Units
            if(Units.objects.filter(Name = unit).first() is None):
                unitInstance = Units(
                    Name = unit
                )
                unitInstance.save()
            # Insert unit and UnitID into ShowUnitRoles
            showUnitRoleInstance = ShowUnitRoles(
                ShowID = showInstance, 
                UnitID = Units.objects.filter(Name = unit).first(), 
                Role = unitType
            )
            showUnitRoleInstance.save()
