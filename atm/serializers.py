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
        transaction_type = data.get("transaction_type")
        amount = data.get("amount")
        source_account = Account.objects.get(id=data.get("source").id)

        if transaction_type in ["withdraw", "send"]:
            if amount > source_account.balance:
                raise serializers.ValidationError("You have insufficient balance")

        return data