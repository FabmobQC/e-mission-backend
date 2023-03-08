from rest_framework import serializers
from projects.models import Project, Form, FormURL, Notification, NotificationTitles, NotificationMessages


class NotificationMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationMessages
        fields = '__all__'

class NotificationTitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTitles
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):

    titles = NotificationTitlesSerializer(read_only=True, many=True)
    messages = NotificationMessagesSerializer(read_only=True, many=True)

    class Meta:
        model = Notification
        fields = '__all__'

class FormURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormURL
        fields = '__all__'

class FormSerializer(serializers.ModelSerializer):

    urls = FormURLSerializer(read_only=True, many=True)

    class Meta:
        model = Form
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):

    main_form = FormSerializer()
    daily_forms = FormSerializer(read_only=True, many=True)
    daily_notifications = NotificationSerializer(read_only=True, many=True)

    timezone = serializers.SerializerMethodField()

    def get_timezone(self, obj):
        return obj.get_timezone_display()

    class Meta:
        model = Project
        fields = '__all__'