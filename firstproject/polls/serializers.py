from rest_framework import serializers
from .models import CryptoTransaction ,Simbol , TableView


class AllSimbols(serializers.ModelSerializer):
    class Meta:
        model = Simbol
        fields = '__all__'


class CryptoTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoTransaction
        fields = '__all__'



class TableViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableView
        fields = '__all__'

