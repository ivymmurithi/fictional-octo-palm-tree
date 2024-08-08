from django.db import models


class Account(models.Model):
    username = models.CharField(max_length=255, null=False, blank=False, unique=True)
    balance = models.FloatField(default=0, null=False, blank=False)

    def __str__(self):
        return self.username


class Transaction(models.Model):
    transaction_type = models.CharField(max_length=255, null=False, blank=False)
    source = models.ForeignKey(Account, null=False, blank=False, on_delete=models.CASCADE, related_name="sender")
    target = models.ForeignKey(Account, null=True, blank=True, on_delete=models.CASCADE, related_name="reciever")
    amount = models.FloatField(default=0, null=False, blank=False)