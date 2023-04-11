from rest_framework import serializers

from .models import *
from account.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryModel
        fields = '__all__'

        extra_kwargs = {"slug": {"read_only": True}}


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetModel
        fields = '__all__'

        extra_kwargs = {
                "slug": {"read_only": True},
                "user": {"read_only": True}
            }


class AssetDetailSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = AssetModel
        fields = '__all__'
