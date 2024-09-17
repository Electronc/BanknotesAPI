from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from MoneyRecogniser.recogniser import identyfy_bill
from django.core.files.base import ContentFile
from datetime import datetime
import base64
import logging
import io
import requests
#import anonymus user
from django.contrib.auth.models import AnonymousUser
from MoneyRecogniser.serializers import GroupSerializer, UserSerializer, CurrenciesSerializer, DenominationsSerializer, Money_ScanSerializer
from MoneyRecogniser.models import Currencies, Denominations, Money_Scan
from django.db.models import Sum


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class recogniseBill(APIView):

    permission_classes = [permissions.BasePermission]

    def post(self, request, format=None):
        data = request.data
        b64 = False
        image_file = data["image"]
        if "base64" in image_file:
            image_file = image_file.split(",")[1]
            image_file = base64.b64decode(image_file)
            image = io.BytesIO(image_file)
            b64 = True
        else:
            image = image_file
            image_up = image_file
        result = identyfy_bill(image)
        if b64:
            image_up = ContentFile(image.getvalue(), name=result["currency"] + "_" + str(result["denomination"]) + str(datetime.now())+ ".jpg")
        logging.warning(result)
        #Add scan to database
        currencyObject = Currencies.objects.get(currency=result["currency"])
        #denominationObject = Denominations.objects.get(currency=currencyObject, denomination=result["denomination"])
        if request.user.is_authenticated:
            user = request.user
            obj = Money_Scan.objects.create(userId=user, image=image_up, currency=currencyObject, denomination=result['denomination'], confidence=result["confidence"])
        else:
            obj = Money_Scan.objects.create(image=image_up, currency=currencyObject, denomination=result['denomination'], confidence=result["confidence"])
        #add image to result
        result["image"] = obj.image.url
        return Response(
            result
        )


#get money scans for user authenticvated by token
class Money_ScanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Money_Scan to be viewed or edited.
    """
    queryset = Money_Scan.objects.all()
    serializer_class = Money_ScanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Money_Scan.objects.filter(userId=user)

    
class CurrenciesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Currencies to be viewed or edited.
    """
    queryset = Currencies.objects.all()
    serializer_class = CurrenciesSerializer
    permission_classes = [permissions.BasePermission]


class DenominationsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Denominations to be viewed or edited.
    """
    queryset = Denominations.objects.all()
    serializer_class = DenominationsSerializer
    permission_classes = [permissions.BasePermission]


class getUserScanStats(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def askNBP(self, currency):
        api_url = "http://api.nbp.pl/api/exchangerates/rates/a/" + currency + "/?format=json"
        response = requests.get(api_url)
        currency_rate = response.json()["rates"][0]["mid"]
        return currency_rate
        pass

    def get(self, request, format=None):
        user = request.user
        currencies = Currencies.objects.all()
        stats = {}
        for currency in currencies:
            currency_rate = self.askNBP(currency.currency)
            scans_count = Money_Scan.objects.filter(userId=user, currency=currency).count()
            scans_denominations_sum = list(Money_Scan.objects.filter(userId=user, currency=currency).aggregate(Sum('denomination')).values())[0]
            stats[currency.currency] = {
                "scans_count": scans_count,
                "scans_denominations_sum": scans_denominations_sum,
                "currency_rate": currency_rate,
                "total_value": scans_denominations_sum*currency_rate
            }
        return Response(stats)
        