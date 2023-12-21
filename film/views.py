from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import *


# def get(self, request):
#         posts = Post.objects.all()
#         title = request.query_params.get('title')
#         text = request.query_params.get('text')

#         word = request.query_params.get('word')
#         if word is not None:
#             posts1 = posts.filter(title__icontains=word)
#             posts2 = posts.filter(text__icontains=word)
#             posts = posts1.union(posts2)
#         if title:
#             posts = posts.filter(title__icontains=title)
#         if text:
#             posts = posts.filter(text__icontains=text)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
class AktyorlarApi(APIView):
    def get(self, request):
        pagination_class = PageNumberPagination
        pagination_class.page_size = 1
        paginator = PageNumberPagination()
        aktyorlar = Aktyor.objects.all()
        natija = paginator.paginate_queryset(aktyorlar, request)
        ism = request.query_params.get('ism')
        davlat = request.query_params.get('davlat')

        qidiruv = request.query_params.get('qidiruv')
        if qidiruv:
            aktyorlar = Aktyor.objects.annotate(
                oxshashlik = TrigramSimilarity('ism', qidiruv))
            aktyorlar = aktyorlar.filter(davlat__icontains=davlat)
        serializers = AktyorSerializer(natija, many=True)
        return Response(serializers.data)
    
    def post(self, request):
        aktyor = request.data
        serializer = AktyorSerializer(data=aktyor)
        if serializer.is_valid():
            valid = serializer.validated_data
            Aktyor.objects.create(
                ism = valid.get('ism'),
                tugilgan_yil = valid.get('tugilgan_yil'),
                davlat = valid.get('davlat'),
                jins = valid.get('jins')
            )
            return Response({"success": 'True'})
        return Response(serializer.errors)
    



class AktyorApi(APIView):
    def get(self, request, pk):
        aktyor = Aktyor.objects.get(id=pk)
        serializer = AktyorSerializer(aktyor)
        return Response(serializer.data)
    
    def update(self, request, pk):
        data = request.data
        aktyor = Aktyor.objects.get(id=pk)
        serializer = AktyorSerializer(aktyor, data=data)
        if serializer.is_valid():
            aktyor.update(
                davlat = serializer.validated_data.get('davlat')
            )
            return Response({'success': 'True'})
        return Response(serializer.errors) 
    


class TariflarApi(APIView):
    def get(self, request):
        tariflar = Tarif.objects.all()
        serializer = TarifSerializer(tariflar, many=True)
        return Response(serializer.data)
    def post(self, request):
        tarif = request.data
        serializer = TarifSerializer(data=tarif)
        if serializer.is_valid():
            valid = serializer.validated_data
            Tarif.objects.create(
                nom = valid.get('nom'),
                narx = valid.get('narx'),
                davomiylik = valid.get('davomiylik')
            )
            return Response({"success": 'True'})
        return Response(serializer.errors)
    
class TarifApi(APIView):
    def get(self, request, pk):
        aktyor = Tarif.objects.get(id=pk)
        serializer = TarifSerializer(aktyor)
        return Response(serializer.data)
    
    def update(self, request, pk):
        data = request.data
        tarif = Tarif.objects.filter(id=pk)
        serializer = Tarif(tarif, data=data)
        if serializer.is_valid():
            valid = serializer.validated_data
            tarif.update(
                nom = valid.get('nom'),
                narx = valid.get('narx'),
                davomiylik = valid.get('davomiylik')
            )
            return Response({'success': 'True'})
        return Response(serializer.errors) 
    
    def delete(self, request, pk):
        Tarif.objects.get(id=pk).delete()
        return Response({"success": 'True'})
    
class KinolarApi(APIView):
    def get(self, request):
        kinolar = Kino.objects.all()
        serializer = KinoSerializer(kinolar, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        kino = request.data
        serializer = KinoPostSerializer(data=kino)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class KinoApi(APIView):
    def get(self, request, pk):
        kino = Kino.objects.get(id=pk)
        serializer = KinoSerializer(kino)
        return Response(serializer.data)
    
class IzohApi(viewsets.ModelViewSet):
    filter_backends = [OrderingFilter]
    ordering_fields = ['sana']
    queryset = Izoh.objects.all()
    serializer_class = IzohSerializerr

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Izoh.objects.all()
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IzohDestroyRetireveUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Izoh.objects.all()
    serializer_class = IzohSerializerr

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        result = get_object_or_404(Izoh, id=self.kwargs['pk'], user=self.request.user)
        return result
    
    def perform_destroy(self, instance):
        if instance.user == self.request.user():
            isinstance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Izoh sizga tegishli emas"})
