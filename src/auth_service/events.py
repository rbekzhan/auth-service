import attr
import uuid
import typing as t


@attr.define
class RegisterEvent:
    username: str = attr.ib(validator=attr.validators.instance_of(str))
    first_name: str = attr.ib(validator=attr.validators.instance_of(str))
    last_name: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.define
class VerifyCodeEvent:
    phone_number: str = attr.ib(validator=attr.validators.instance_of(str))
    code: str = attr.ib(validator=attr.validators.instance_of(str))


@attr.define
class UserProfileEvent:
    user_id: uuid = attr.ib(validator=attr.validators.instance_of(str))
    username: str = attr.ib(validator=attr.validators.instance_of(str))
    name: str = attr.ib(default=None, validator=attr.validators.instance_of((str, type(None))))
    surname: str = attr.ib(default=None, validator=attr.validators.instance_of((str, type(None))))
    avatar_path: str = attr.ib(default=None, validator=attr.validators.instance_of((str, type(None))))
    email: str = attr.ib(default=None, validator=attr.validators.instance_of((str, type(None))))
    bio: str = attr.ib(default=None, validator=attr.validators.instance_of((str, type(None))))


@attr.define
class ContactEvent:
    user_id: uuid = attr.ib(validator=attr.validators.instance_of(str))
    phone_number: str = attr.ib(validator=attr.validators.instance_of(str))
    name: str = attr.ib(default=None, validator=attr.validators.instance_of((str, type(None))))
    surname: str = attr.ib(default=None, validator=attr.validators.instance_of((str, type(None))))


@attr.define
class ContactsEvent:
    user_id: uuid = attr.ib(validator=attr.validators.instance_of(str))
    phone_number: t.List[str] = attr.ib(validator=attr.validators.instance_of(list))
    name: str = attr.ib(default=None, validator=attr.validators.instance_of((str, type(None))))
    surname: str = attr.ib(default=None, validator=attr.validators.instance_of((str, type(None))))
