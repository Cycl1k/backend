from equipment.serializer import TypeEquipmentSerializer, EquipmentSerializer
from equipment.models import TypeEquipmentModel, EquipmentsModel

import re


def searchMask(name):
    """
    Поиск ID и маски оборудования по ID или имени устройсва \n
    На вход принимает ID (int) или имя (str) \n
    На выход возвращяет ID и маску серийного номера \n
    Если такого оборудования нет в БД, то возращает имя и 'SN_NO' \n
    """
    try:
        if type(name)!=int:
            print("-- It's not int")
            typeToName = TypeEquipmentModel.objects.filter(nameSl=name)
            serializedName = TypeEquipmentSerializer(typeToName, many=True)
            print('-- ', serializedName.data[0]['id'], serializedName.data[0]['maskSNSl'])
            return serializedName.data[0]['id'], serializedName.data[0]['maskSNSl']
        else:
            print("-- It's int")
            typeToName = TypeEquipmentModel.objects.filter(id=int(name))
            serializedName = TypeEquipmentSerializer(typeToName, many=True)
            print('-- ', name, serializedName.data)
            return name, serializedName.data[0]['maskSNSl']
    except Exception as error:
        print(error)
        return name, 'SN_NO'
    
def validation(id, mask, sn):
    """
    Валидация и сериализация данных \n
    На вход ID оборудования, маску серийного номера и серийный номер \n
    На выходе возращяет list с данными об оборудовании \n
    Если серийный номер не проходит валидацию на основе маски, то возращяет ошибку '-!' \n
    """
    maskSN = mask.replace('N','[0-9]').replace('a', '[a-z]').replace('X', '[a-z0-9]').replace('Z', '[- @]').replace('A', '[A-Z]')
    mat = re.fullmatch(maskSN, sn)
    if mat!=None:
        print('-! Validation Good')
        objt = EquipmentsModel.objects.filter(idNameSl=id, serialNumberSl=sn)
        serializer = EquipmentSerializer(objt, many=True)
        return serializer.data
    print('-! Error validation')
    return '-!'