from django.http import Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets

from equipment.serializer import TypeEquipmentSerializer, EquipmentSerializer
from equipment.models import TypeEquipmentModel, EquipmentsModel

from equipment.companents import searchMask, validation

class TypeEquipmentAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Endpoint \n
        В Headers необходимо указать токен авторизации \n
        Возращает список типов оборудования
        """
        ids = request.query_params.get('id')
        names = request.query_params.get('name')
        
        if ids is not None and names is not None:
            objs = TypeEquipmentModel.objects.filter(id=ids, nameSl=names)
            print("don't none")
        elif names is None and ids is not None:
            objs = TypeEquipmentModel.objects.filter(id=ids)
            print('name')
        elif names is not None and ids is None:
            objs = TypeEquipmentModel.objects.filter(nameSl=names)
            print('ids')
        else:
            objs = TypeEquipmentModel.objects.all()
            print('all')

        serializer = TypeEquipmentSerializer(objs, many=True)

        outer = []
        for elem in serializer.data:
            outer.append({'id': elem['id'],
                          'name': elem['nameSl']})
        return Response(outer, status=status.HTTP_200_OK)
    
class EquipmentAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *agrs, **kwargs):
        """
        Endpoint \n
        В Headers необходимо указать токен авторизации \n
        Возращает список оборудования
        """
        ids = request.query_params.get('id')
        serial = request.query_params.get('serial')
        
        if ids is not None and serial is not None:
            objs = EquipmentsModel.objects.filter(idNameSl=ids, serialNumberSl=serial)
            print("don't none")
        elif serial is None and ids is not None:
            objs = EquipmentsModel.objects.filter(idNameSl=ids)
            print('name')
        elif serial is not None and ids is None:
            objs = EquipmentsModel.objects.filter(serialNumberSl=serial)
            print('ids')
        else:
            objs = EquipmentsModel.objects.all()
            print('all')
        serializer = EquipmentSerializer(objs, many=True)
        outer = []
        for elem in serializer.data:
            outer.append({'id': elem['idNameSl'],
                          'serial': elem['serialNumberSl']})
        return Response(outer, status=status.HTTP_200_OK)


    def post(self, request):
        """
        Endpoint \n
        В Headers необходимо указать токен авторизации \n
        Создает записи в таблицу оборудования \n
        На вход принимает список
        """
        errorList = []
        for num in request.data:
            print('------------------------------------')
            print(num)
            
            sourceName = num['id_name']
            sourceSN = num['serial']

            equipmentID, equipmentMask = searchMask(sourceName)
            if equipmentMask == 'SN_NO':
                errorList.append({'id or name': equipmentID,
                                  'serial number': sourceSN,
                                  'comment': 'Type unknown'})
                print('Good buy!')
                continue
            
            validTrue = validation(equipmentID, equipmentMask, sourceSN)
            if validTrue != []:
                errorList.append({'id or name': sourceName,
                                  'serial number': sourceSN,
                                  'comment': 'Equipment in BD'})
                print('Good buy!')
                continue            
            
            try:
                comment = num['comment']
            except KeyError:
                comment = 'No comments'

            data = {'idNameSl': equipmentID,
                    'serialNumberSl': sourceSN,
                    'commentSl': comment}

            serializer = EquipmentSerializer(data=data)
            print(data)
            if serializer.is_valid():
                serializer.save()  
                print('Saved')
            else:
                print('Failed serialized')
        if errorList == []:
            return Response(data= 'All add in DB', status=status.HTTP_201_CREATED)
        else:
            return Response(data=errorList, status=status.HTTP_200_OK)
    
class EquipmentAPIViewList(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, id):
        """
        Endpoint \n
        В Headers необходимо указать токен авторизации \n
        Возвращает данние об оборуднии \n
        Необходима сериализация данных
        """
        try:
            return EquipmentsModel.objects.get(id=id)
        except EquipmentsModel.DoesNotExist:
            return None
        
    def get(self, request, id):
        """
        Endpoint \n
        В Headers необходимо указать токен авторизации \n
        Возращяет данные об устройстве по ID
        """
        objt = self.get_object(id)
        if not objt:
            return Response({'ID out in range'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EquipmentSerializer(objt)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self,request, id):
        """
        Endpoint \n
        В Headers необходимо указать токен авторизации \n
        Обновляет данные об устройстве по ID \n
        В body может быть указаны, как все данные, так и только часть \n
        Защита от дупликации данных \n
        """
        objt = self.get_object(id)
        if not objt:
            return Response({'ID for update out in range'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            newName = request.data['id_name']
        except KeyError:
            newName = serializer.data['idNameSl']

        cheacker = EquipmentsModel.objects.filter(serialNumberSl = request.data['serial'])
        cheackerSerializer = EquipmentSerializer(cheacker, many=True)
        if cheackerSerializer.data != []:
            return Response({'id or name': newName,
                            'serial number': '',
                            'comment': '',
                            'error': 'Duplicate'})

        serializer = EquipmentSerializer(objt)
        print(serializer.data)

        
        try:
            newSN = request.data['serial']
        except KeyError:
            newSN = serializer.data['serialNumberSl']
        try:
            comment = request.data['comment']
        except KeyError:
            comment = serializer.data['commentSl']

        print('=-', newName, newSN, comment)        
        
        equipmentID, equipmentMask = searchMask(newName)
        print('=- ', equipmentMask)

        if equipmentMask == 'SN_NO':
            return Response({'id or name': newName,
                            'serial number': '',
                            'comment': '',
                            'error': 'Type unknown'})
        
        validTrue = validation(equipmentID, equipmentMask, newSN)
        if validTrue == '-!':
            return Response({'id or name': newName,
                            'serial number': newSN,
                            'comment': comment,
                            'error': 'Validation error'})
        
        data = {'idNameSl': equipmentID,
                'serialNumberSl': newSN,
                'commentSl': comment}

        serializer = EquipmentSerializer(instance=objt, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        """
        Endpoint \n
        В Headers необходимо указать токен авторизации \n
        Удаление данных по ID
        """
        objt = self.get_object(id)
        if not objt:
            return Response({'ID for delete out in range'}, status=status.HTTP_400_BAD_REQUEST)
        objt.delete()
        return Response({id: 'Object delete!'}, status=status.HTTP_200_OK)
        
        