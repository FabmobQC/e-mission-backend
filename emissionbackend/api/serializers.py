from rest_framework import serializers
from projects.models import Project, Form, FormURL, Notification, NotificationTitles, NotificationMessages, Mode, ModeTranslation, Purpose, PurposeTranslation
from userprofile.models import UserProfile


#### Notifications ####
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

#### Modes ####


class ModeTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeTranslation
        fields = '__all__'


class ModesSerializer(serializers.ModelSerializer):
    texts = ModeTranslationSerializer(read_only=True, many=True)

    class Meta:
        model = Mode
        fields = '__all__'

#### Purpose ####


class PurposeTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurposeTranslation
        fields = '__all__'


class PurposeSerializer(serializers.ModelSerializer):
    texts = PurposeTranslationSerializer(read_only=True, many=True)

    class Meta:
        model = Purpose
        fields = '__all__'

#### Forms ####


class FormURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormURL
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):

    urls = FormURLSerializer(read_only=True, many=True)

    class Meta:
        model = Form
        fields = '__all__'

#### Projects ####


class ProjectSerializer(serializers.ModelSerializer):

    main_form = FormSerializer()
    daily_forms = FormSerializer(read_only=True, many=True)
    daily_notifications = NotificationSerializer(read_only=True, many=True)
    modes = serializers.SerializerMethodField()
    purposes = serializers.SerializerMethodField()

    timezone = serializers.SerializerMethodField()

    def get_modes(self, obj):
        modes = obj.modes.all().order_by('projectmode__order')
        return ModesSerializer(many=True, instance=modes).data

    def get_purposes(self, obj):
        purposes = obj.purposes.all().order_by('projectpurpose__order')
        return PurposeSerializer(many=True, instance=purposes).data

    def get_timezone(self, obj):
        return obj.get_timezone_display()

    class Meta:
        model = Project
        fields = '__all__'


#### UserProfile ####
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'
