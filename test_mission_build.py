import pytest
from message_system import MessageType

from mission_build import (
    Officier,
    officier_dwarkaar,
    officier_bougle,
    officier_klein,
    officier_braun,
    officier_weber,
    sample_messages,
    rank_values,
)

def test_officier_attributes():
    o = Officier("Captain", "Testname", "Testunit", "img1", "img2", "img3")
    assert o.rank == "Captain"
    assert o.name == "Testname"
    assert o.unit == "Testunit"
    assert o.image1 == "img1"
    assert o.image2 == "img2"
    assert o.image3 == "img3"

def test_get_rank_value_known():
    assert officier_dwarkaar.get_rank_value() == rank_values["Captain"]
    assert officier_bougle.get_rank_value() == rank_values["General"]
    assert officier_klein.get_rank_value() == rank_values["Leutnand"]
    assert officier_braun.get_rank_value() == rank_values["Captain"]
    assert officier_weber.get_rank_value() == rank_values["Major"]

def test_get_rank_value_unknown():
    o = Officier("UnknownRank", "X", "Y", "a", "b", "c")
    assert o.get_rank_value() == 0

def test_sample_messages_structure():
    messages = sample_messages()
    assert len(messages) == 4
    for msg in messages:
        assert hasattr(msg, "type")
        assert hasattr(msg, "sender")
        assert hasattr(msg, "time")
        assert hasattr(msg, "content")

def test_sample_messages_content():
    messages = sample_messages()
    assert messages[0].type == MessageType.WITNESSED
    assert messages[0].sender == officier_dwarkaar.name
    assert "Fernglas" in messages[0].content

    assert messages[1].type == MessageType.NORMAL
    assert messages[1].sender == officier_weber.name
    assert "linke Flügel" in messages[1].content

    assert messages[2].type == MessageType.URGENT
    assert messages[2].sender == officier_braun.name
    assert "Position Delta" in messages[2].content

    assert messages[3].type == MessageType.NORMAL
    assert messages[3].sender == officier_klein.name
    assert "Kavallerie" in messages[3].content

def test_rank_values_dict():
    assert rank_values["Korporal"] == 1
    assert rank_values["Leutnand"] == 2
    assert rank_values["Major"] == 3
    assert rank_values["Captain"] == 4
    assert rank_values["General"] == 5

test_rank_values_dict()