class SerializerContextMixin:
    def get_serializer_context(self):
        return {'request': self.request}