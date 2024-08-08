from .models import Account, Transaction
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def validate(self, data):
        if data["transaction_type"] == "withdraw" or "send" and data["amount"] >= data["source"].balance:
            raise serializers.ValidationError("You have insufficient balance")
        return data