from marshmallow import EXCLUDE, post_load, fields, Schema

from auth_service.events import RegisterEvent, VerifyCodeEvent, UserProfileEvent, ContactEvent


class UserProfileSchema(Schema):
    user_id: str = fields.Str()
    username: str = fields.Str()
    first_name: str = fields.Str()
    last_name: str = fields.Str()
    bio: str = fields.Str(default=None)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data, **kwargs):
        return UserProfileEvent(**data)


class VerifyCodeSchema(Schema):
    phone_number: str = fields.Str()
    code: str = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load()
    def make_object(self, data, **kwargs):
        return VerifyCodeEvent(**data)


class ContactSchema(Schema):
    user_id: str = fields.Str()
    phone_number: str = fields.Str()
    first_name: str = fields.Str()
    last_name: str = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load()
    def make_object(self, data, **kwargs):
        return ContactEvent(**data)


class GetAccountWithContact(Schema):
    user_id: str = fields.Str()
    username: str = fields.Str()
    first_name: str = fields.Str()
    last_name: str = fields.Str()

