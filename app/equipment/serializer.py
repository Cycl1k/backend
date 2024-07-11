from rest_framework import serializers
from equipment.models import TypeEquipmentModel, EquipmentsModel

class TypeEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeEquipmentModel
        fields = ['id', 'nameSl', 'maskSNSl']

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentsModel
        fields = ['id','idNameSl', 'serialNumberSl', 'commentSl']