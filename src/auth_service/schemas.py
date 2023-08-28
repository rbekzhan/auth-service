import typing as t

from marshmallow import EXCLUDE, post_load, fields, Schema
from auth_service.events import VerifyCodeEvent, UserProfileEvent, ContactEvent, ContactsEvent


class UserProfileSchema(Schema):
    user_id: str = fields.Str()
    username: str = fields.Str()
    name: str = fields.Str()
    surname: str = fields.Str()
    bio: str = fields.Str(default=None)
    email: str = fields.Str(default=None)
    avatar_path: str = fields.Str(default=None)

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
    name: str = fields.Str()
    surname: str = fields.Str()

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
    avatar_path: str = fields.Str()


class GetAccountInfoById(Schema):
    user_id: str = fields.Str()
    username: str = fields.Str()
    avatar_path: str = fields.Str()
    first_name: str = fields.Str()
    last_name: str = fields.Str()
    bio: str = fields.Str()


class ContactsSaveSchema(Schema):
    user_id: str = fields.Str()
    phone_number: t.List = fields.List(fields.Str)
    name: str = fields.Str()
    surname: str = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load()
    def make_object(self, data, **kwargs):
        return ContactsEvent(**data)
