from rest_framework import serializers
from Metten.years.models import Adder


class AdderSerializer(serializers.HyperlinkedModelSerializer):
    api_url = serializers.SerializerMethodField('get_api_url')
    start_date = serializers.Field(source="start")
    end_date = serializers.Field(source="end")

    class Meta:
        model = Adder
        fields = ('id', 'title', 'description', 'is_completed', 'content_type', 'date', 'start_date', 'end_date', 'url')
        read_only_fields = ('id', 'title')

    def get_api_url(self, obj):
        return "#/api/adder/%s" % obj.id