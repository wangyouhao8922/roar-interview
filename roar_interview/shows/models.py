from django.db import models

class Shows(models.Model):
    Version = models.CharField(max_length=10)
    ShowID = models.AutoField(primary_key=True)
    UID = models.CharField(max_length=50, unique=True)
    Title = models.CharField(max_length=100)
    Category = models.CharField(max_length=10)
    ShowUnit = models.CharField(max_length=200, null=True, blank=True)
    DiscountInfo = models.CharField(max_length=500, null=True, blank=True)
    DescriptionFilterHtml = models.CharField(max_length=3000, null=True, blank=True)
    ImageUrl = models.CharField(max_length=300, null=True, blank=True)
    WebSales = models.CharField(max_length=300, null=True, blank=True)
    SourceWebPromote = models.CharField(max_length=300, null=True, blank=True)
    Comment = models.CharField(max_length=3000, null=True, blank=True)
    EditModifyDate = models.DateTimeField(null=True, blank=True)
    SourceWebName = models.CharField(max_length=50)
    StartDate = models.DateField()
    EndDate = models.DateField()
    HitRate = models.IntegerField()

    def __str__(self):
        return self.Title

class Locations(models.Model):
    LocationID = models.AutoField(primary_key=True)
    Address = models.CharField(max_length=300)
    Name = models.CharField(max_length=100)
    Latitude = models.FloatField(null=True, blank=True)
    Longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.Name

class ShowInfos(models.Model):
    ShowInfoID = models.AutoField(primary_key=True)
    ShowID = models.ForeignKey(Shows, on_delete=models.CASCADE)
    Time = models.DateTimeField()
    LocationID = models.ForeignKey(Locations, on_delete=models.PROTECT)
    OnSales = models.CharField(max_length=1)
    Price = models.CharField(max_length=300, null=True, blank=True)
    EndTime = models.DateTimeField()

    def __str__(self):
        return str(self.Time)

class Units(models.Model):
    UnitID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=30)

    def __str__(self):
        return self.Name

class ShowUnitRoles(models.Model):
    ShowUnitRoleID = models.AutoField(primary_key=True)
    ShowID = models.ForeignKey(Shows, on_delete=models.CASCADE)
    UnitID = models.ForeignKey(Units, on_delete=models.PROTECT)
    Role = models.CharField(max_length=20)

    def __str__(self):
        return str(self.ShowID)

