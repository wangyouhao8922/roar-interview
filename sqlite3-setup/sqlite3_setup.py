import sqlite3
import json

conn = sqlite3.connect('RoarInterview.db')

# conn.execute("PRAGMA foreign_keys = ON")
# create a cursor
# cursor = conn.execute("select ")
cursor = conn.cursor()

# create all table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Shows (
        Version     REAL        NOT NULL,
        ShowID      INTEGER     PRIMARY KEY,
        UID         TEXT        NOT NULL,
        Title       TEXT        NOT NULL,
        Category    INTEGER     NOT NULL,
        ShowUnit    INTEGER     ,
        DiscountInfo  INTEGER     ,
        DescriptionFilterHtml TEXT,
        ImageUrl    TEXT        ,
        WebSales    INTEGER     , 
        SourceWebPromote TEXT   ,
        Comment     TEXT        ,
        EditModifyDate TEXT     ,
        SourceWebName INTEGER   NOT NULL, 
        StartDate   TEXT        NOT NULL, 
        EndDate     TEXT        NOT NULL, 
        HitRate     INTEGER     NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ShowInfos (
        ShowInfoID  INTEGER     PRIMARY KEY,
        ShowID      INTEGER     NOT NULL, 
        Time        TEXT        NOT NULL,
        LocationID  INTEGER     NOT NULL,
        OnSales     TEXT        NOT NULL, 
        Price       TEXT, 
        EndTime     TEXT        NOT NULL,
        FOREIGN KEY (ShowID) REFERENCES Shows (ShowID),
        FOREIGN KEY (LocationID) REFERENCES Locations (LocationID)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Locations (
        LocationID  INTEGER     PRIMARY KEY, 
        Address     TEXT        NOT NULL,
        Name        TEXT        NOT NULL,
        Latitude    REAL,
        Longitude   REAL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Units (
        UnitID      INTEGER     PRIMARY KEY,
        Name        TEXT        NOT NULL
    )
""")
               
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ShowUnitRoles (
        ShowUnitRoleID INTEGER  PRIMARY KEY,
        ShowID      INTEGER     NOT NULL,
        UnitID      INTEGER     NOT NULL,
        Role        TEXT        NOT NULL,
        FOREIGN KEY (ShowID) REFERENCES Shows (ShowID),
        FOREIGN KEY (UnitID) REFERENCES Units (UnitID)
    )
""")

# insert data from shows-data.json
with open('/Users/wangyouhao/Desktop/roar-interview/roar_interview/shows-data.json', 'r') as shows:
    showList = json.load(shows)

# declare map for recording unique value in show and their id in table. 
locationAddressToID = {}
UnitNameToID = {}

# declare list for iterate through units
unitTypeList = ['masterUnit', 'subUnit', 'supportUnit', 'otherUnit']

# Insert showList
for show in showList:
    # Insert show into Shows
    cursor.execute(
        """INSERT INTO Shows (Version, UID, Title, Category, ShowUnit, DiscountInfo, DescriptionFilterHtml, ImageUrl, WebSales, SourceWebPromote, Comment, EditModifyDate, SourceWebName, StartDate, EndDate, HitRate) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
        (show['version'], show['UID'], show['title'], show['category'], show['showUnit'], show['discountInfo'], show['descriptionFilterHtml'], show['imageUrl'], show['webSales'], show['sourceWebPromote'], show['comment'], show['editModifyDate'], show['sourceWebName'], show['startDate'], show['endDate'], show['hitRate'])
    )
    showID = cursor.lastrowid

    # Insert showInfo
    for info in show['showInfo']:
        # Insert unique location into Locations
        if info['location'] not in locationAddressToID:
            cursor.execute(
                'INSERT INTO Locations (Address, Name, Latitude, Longitude) VALUES (?, ?, ?, ?)', (info['location'], info['locationName'], info['latitude'], info['longitude'])
            )
            locationAddressToID[info['location']] = cursor.lastrowid

        # Insert showInfo and LocationID into ShowInfos
        cursor.execute(
            """INSERT INTO ShowInfos (ShowID, Time, LocationID, OnSales, Price, EndTime) 
            VALUES (?, ?, ?, ?, ?, ?)""", 
            (showID, info['time'], locationAddressToID[info['location']], info['onSales'], info['price'], info['endTime'])
        )

    # Insert masterUnit, subUnit, supportUnit and otherUnit into Units
    for unitType in unitTypeList:
        for unit in show[unitType]:
            # Insert unique unit into Units
            if unit not in UnitNameToID:
                cursor.execute(
                    'INSERT INTO Units (Name) VALUES (?)', (unit,)
                )
                UnitNameToID[unit] = cursor.lastrowid

            # Insert unit and UnitID into ShowUnitRoles
            cursor.execute(
                """INSERT INTO ShowUnitRoles (ShowID, UnitID, Role) 
                VALUES (?, ?, ?)""", 
                (showID, UnitNameToID[unit], unitType)
            )

conn.commit()
conn.close()