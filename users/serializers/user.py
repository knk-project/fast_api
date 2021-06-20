from core.serializer import Serializer


class UserSerializer(Serializer):
    exclude = ('is_active', 'hashed_password',)


class UserFullDataSerializer(Serializer):
    exclude = ('hashed_password',)
