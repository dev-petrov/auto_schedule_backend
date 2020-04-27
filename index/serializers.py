from rest_framework import serializers
from index.models import ConstraintCollection, Flow


class ConstraintCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstraintCollection
        fields = '__all__'


class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = '__all__'
