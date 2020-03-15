from rest_framework import serializers
from index.models import ConstraintCollection


class ConstraintCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstraintCollection
        fields = '__all__'


