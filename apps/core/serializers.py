from rest_framework import serializers

from apps.core.utils import send_email_job_registration


class SendContactUsEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    message = serializers.CharField(max_length=255)

    @staticmethod
    def send_mail(validated_data):
        send_email_job_registration(
            'Docker',
            'levonstdev@gmail.com',
            'contact_us',
            {
                'email': validated_data['email'],
                'name': validated_data['name'],
                'message': validated_data['message'],
            },
            'Your request has been received',
        )
        
        send_email_job_registration(
            'Docker',
            validated_data['email'],
            'contact_us-pending',
            {
                'email': validated_data['email'],
                'name': validated_data['name'],
                'message': validated_data['message'],
            },
            'Your request has been received',
        )
