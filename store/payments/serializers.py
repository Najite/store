from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        # [
        #     'id',
        #     'reference',
        #     'user',
        #     'amount',
        #     'created_at'
        # ]

     