from django.db import models

class PersonalData(models.Model):
    national_id=models.CharField(max_length=11,null=False,blank=False,unique=True)
    first_name = models.CharField(max_length=20,null=False, blank=False)
    last_name = models.CharField(max_length=20,null=False, blank=False)
    def __str__(self):
        return self.first_name + " "+self.last_name

    


