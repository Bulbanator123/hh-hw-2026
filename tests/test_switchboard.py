import pytest

from app.switchboard import Switchboard
from app.users import ForeignUser, LocalUser


def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_register_call_not_six_arguments_in_raw() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="Слишком мало аргументов"):
        switchboard.register_call("1,Ivan,+79990000000,2,John")


def test_register_check_with_invalid_id() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="В строке есть невалидное айди"):
        switchboard.register_call("NOT_ID,Ivan,+79990000000,2,John,+15550000000")


def test_register_check_with_invalid_name() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="В строке есть невалидное имя"):
        switchboard.register_call("1,I1v4an,+79990000000,2,John,+15550000000")


def test_register_check_with_invalid_phone() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="В строке есть невалидный телефон"):
        switchboard.register_call("1,Ivan,+79990000000,2,John,+155fefef")


def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1


def test_switchboard_check_initial_state() -> None:
    switchboard = Switchboard()
    assert switchboard.get_active_calls_count() == 0
    assert switchboard.get_cross_border_calls_count() == 0
