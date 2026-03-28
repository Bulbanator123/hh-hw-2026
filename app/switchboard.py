from __future__ import annotations

from dataclasses import dataclass

from app.users import User, LocalUser, ForeignUser

LOCAL_PHONE_PREFIX = "+7"


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []
        self._count_cross_border_calls: int = 0

    def get_active_calls(self) -> list[ActiveCall]:
        return self._active_calls

    def add_to_active_calls(self, active_call: ActiveCall) -> ActiveCall:
        self._active_calls.append(active_call)
        if active_call.is_cross_border:
            self._count_cross_border_calls += 1
        return active_call

    @staticmethod
    def create_user(id: int, name: str, phone: str) -> User:
        id = int(id)
        if phone.startswith(LOCAL_PHONE_PREFIX):
            return LocalUser(id=id, fullname=name, phone=phone)
        return ForeignUser(id=id, fullname=name, phone=phone)

    @staticmethod
    def validate_phone(phone: str) -> bool:
        return phone.startswith("+") and phone[1:].isdigit()

    @staticmethod
    def validate_name(name: str) -> bool:
        return name.replace(" ", "").isalpha()

    @staticmethod
    def validate_id(id) -> bool:
        if isinstance(id, str) and id.isdigit() or isinstance(id, int):
            return int(id) > 0
        return False

    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,reciever_id,reciever_name,reciever_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"
        '''

        list_call = raw_call.split(",")

        if len(list_call) != 6:
            raise ValueError("Слишком мало аргументов в строке")

        caller_id, caller_name, caller_phone = list_call[:3]
        receiver_id, receiver_name, receiver_phone = list_call[3:]

        if not self.validate_id(caller_id) or not self.validate_id(receiver_id):
            raise ValueError("В строке есть невалидное айди")

        if not self.validate_name(caller_name) or not self.validate_name(receiver_name):
            raise ValueError("В строке есть невалидное имя")

        if not self.validate_phone(caller_phone) or not self.validate_phone(receiver_phone):
            raise ValueError("В строке есть невалидный телефон")

        caller: User = self.create_user(id=int(caller_id), name=caller_name, phone=caller_phone)
        receiver: User = self.create_user(id=int(receiver_id), name=receiver_name, phone=receiver_phone)

        active_call = ActiveCall(caller=caller, receiver=receiver)
        return self.add_to_active_calls(active_call)

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return self._count_cross_border_calls
