#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from rest_framework import serializers
from userprofile.models import User
from rest_framework.utils import model_meta
from projects.models import Project


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'project', 'date_joined')
        required_fields = ('username', 'email', 'password', 'project')

        # These fields are displayed but not editable and have to be a part of 'fields' tuple
        read_only_fields = ('is_active', 'is_staff',
                            'is_superuser', 'date_joined')

        # Use extra_kwargs to specify which fields configuration
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 4},
            'date_joined': {'read_only': True},
        }

    def get_fields(self, *args, **kwargs):
        fields = super(UserSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) in ["PUT", "PATCH"]:
            fields['password'].required = False
        return fields

    def create(self, validated_data):
        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        many_to_many = {}
        info = model_meta.get_field_info(ModelClass)
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(**validated_data)
        except TypeError:
            tb = serializers.traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance

    def update(self, instance, validated_data):
        """ Update fields """
        ModelClass = self.Meta.model

        to_many_fields = [
            field.name for field in ModelClass._meta.many_to_many]

        for attr, value in validated_data.items():
            if attr in to_many_fields:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    """[MOBILE] Login serializer for residents."""

    username = serializers.CharField(
        label="Username",
        allow_blank=False,
        required=True,
    )

    password = serializers.CharField(
        label="Password",
        required=True
    )

    project = serializers.IntegerField(
        label="Project ID",
        required=True,
    )
