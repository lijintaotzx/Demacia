from django.contrib.auth.models import User
from rest_framework import serializers

from lib.phonenum_check import check_phone_num
from .models import UserProfile


class UserSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    password1 = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128)

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError('password1 must equal with password2!')

        filterResult = User.objects.filter(username=attrs['username'])
        if len(filterResult) > 0:
            raise serializers.ValidationError('user already exists')

        return attrs


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)


class UserpeofileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        # fields = '__all__'
        exclude = ('user','id')


    def update(self, instance, validated_data):
        print validated_data
        instance.phone_num = validated_data.get('phone_num',instance.phone_num)
        instance.sex = validated_data.get('sex',instance.sex)
        instance.address = validated_data.get('address',instance.address)
        instance.age = validated_data.get('age',instance.age)
        instance.email = validated_data.get('email',instance.email)
        instance.descr = validated_data.get('descr',instance.descr)
        instance.head_photo = validated_data.get('head_photo',instance.head_photo)
        instance.save()
        return instance

    def validate_phone_num(self, attrs):
        if not check_phone_num(attrs):
            raise serializers.ValidationError('phone_num must be a phone number!')
        return attrs

    def validate_sex(self, attrs):
        if attrs not in ('man','woman'):
            raise serializers.ValidationError('sex must in ("man","woman")!')
        return attrs


