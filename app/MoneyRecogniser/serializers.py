from django.contrib.auth.models import Group, User
from rest_framework import serializers
from MoneyRecogniser.models import Currencies, Denominations, Money_Scan


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CurrenciesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Currencies
        fields = ['currency', 'description','symbol','name']

class DenominationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Denominations
        fields = ['denominationID','currency', 'denomination', 'description']

class Money_ScanSerializer(serializers.HyperlinkedModelSerializer):

    currency = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='currency'
    )
    class Meta:
        model = Money_Scan
        fields = ['scanId', 'userId', 'image', 'currency', 'denomination', 'confidence', 'created_at']






