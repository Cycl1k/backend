from django.db import models

class TypeEquipmentModel(models.Model):
    nameSl = models.CharField(max_length=70)
    maskSNSl = models.CharField(max_length = 10)

    def __str__(self):
        return self.nameSl
    
class EquipmentsModel(models.Model):
    idNameSl = models.IntegerField()
    serialNumberSl = models.CharField(max_length = 10)
    commentSl = models.TextField()

    # def __str__(self):
    #     return self.idNameSl