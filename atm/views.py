from rest_framework import viewsets
from rest_framework.response import Response
from .models import Account, Transaction
from django.shortcuts import get_object_or_404
from .serializers import AccountSerializer, TransactionSerializer
from rest_framework.decorators import api_view
from django.db import transaction
from rest_framework.exceptions import ValidationError


@api_view(['POST'])
def deposit(request):
    if request.data["transaction_type"] == "deposit":
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()

        transaction.source.balance += transaction.amount
        transaction.source.save()

        return Response(TransactionSerializer(transaction).data)


@api_view(['POST'])
def withdraw(request):
    if request.data["transaction_type"] == "withdraw":
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()

        transaction.source.balance -= transaction.amount
        transaction.source.save() 

        return Response(TransactionSerializer(transaction).data)


@api_view(['POST'])
def send(request):
    if request.data["transaction_type"] == "send":
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_transaction = serializer.save()

        with transaction.atomic():
            send_transaction.source.balance -= send_transaction.amount
            send_transaction.source.save() 

            send_transaction.target.balance += send_transaction.amount
            send_transaction.target.save()

        return Response(TransactionSerializer(send_transaction).data)
    

class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

