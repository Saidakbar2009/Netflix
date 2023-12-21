from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *

class AktyorSerializer(serializers.Serializer):
    ism = serializers.CharField()
    davlat = serializers.CharField()
    jins = serializers.CharField()
    tugilgan_yil = serializers.DateField()
    def validate_ism(self, attrs):
        if len(attrs) < 4:
            raise ValidationError('kata bola olmaydi')
    def validate_jins(self, attrs):
        if attrs != 'erkak' or attrs != 'ayol':
            raise ValidationError('xato')

class TarifSerializer(serializers.Serializer):
    nom = serializers.CharField()
    narx = serializers.IntegerField()
    davomiylik = serializers.CharField()

class KinoSerializer(serializers.ModelSerializer):
    aktyorlar = AktyorSerializer(many=True)
    class Meta:
        model = Kino
        fields = '__all__'

class KinoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kino
        fields = '__all__'

class IzohSerializerr(serializers.ModelSerializer):
    class Meta:
        model = Izoh
        fields = '__all__'