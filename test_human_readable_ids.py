import pytest
from typing import List

from human_readable_ids import HumanReadableIdManager


@pytest.fixture
def manager_seed_0() -> HumanReadableIdManager:
    return HumanReadableIdManager()


@pytest.fixture
def manager_seed_42() -> HumanReadableIdManager:
    return HumanReadableIdManager(seed=42)


@pytest.fixture
def original_ids() -> List[str | int]:
    return ["id0", "test_id", 0, 1, 42, b"test-bytes"]


@pytest.fixture
def unused_ids() -> List[str]:
    return ["unused0", "ununsed1"]


@pytest.fixture
def filled_manager_seed_0(
    manager_seed_0,
    original_ids
) -> HumanReadableIdManager:
    for o in original_ids:
        manager_seed_0.generate_human_readable_id(o)
    return manager_seed_0


@pytest.fixture
def human_readable_ids_seed_0() -> List[str]:
    return [
        "blustery-judo-28",
        "pushchair-font-4",
        "spirits-speech-54",
        "stingily-trimester-1",
        "rake-jubilant-49",
        "unframed-denial-13"
    ]


@pytest.fixture
def human_readable_ids_seed_42() -> List[str]:
    return [
        "backlog-applied-30",
        "imperfect-outreach-61",
        "runway-reference-24",
        "handbook-sacrament-65",
        "glimmer-hatless-8",
        "deeply-showing-19"
    ]


@pytest.fixture
def default_value() -> str:
    return "default-value"


@pytest.fixture
def colliding_original_ids() -> List[bytes]:
    strings = [
        "d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70",  # noqa: E501
        "d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70"  # noqa: E501
    ]
    ints = [int(s, 16) for s in strings]
    return [i.to_bytes(len(s) // 2, 'big') for i, s in zip(ints, strings)]


@pytest.fixture
def non_colliding_human_readable_ids() -> List[str]:
    return ["pasty-never-43", "pasty-never-44"]


def test_generate_correct_ids_0(
    manager_seed_0,
    original_ids,
    human_readable_ids_seed_0
):
    for o, h in zip(original_ids, human_readable_ids_seed_0):
        generated = (
            manager_seed_0.generate_human_readable_id(o)
        )
        assert generated == h


def test_generate_correct_ids_42(
    manager_seed_42,
    original_ids,
    human_readable_ids_seed_42
):
    for o, h in zip(original_ids, human_readable_ids_seed_42):
        generated = (
            manager_seed_42.generate_human_readable_id(o)
        )
        assert generated == h


def test_dont_regenerate(
    manager_seed_0,
    original_ids,
    human_readable_ids_seed_0
):
    for _ in range(2):
        for o, h in zip(original_ids, human_readable_ids_seed_0):
            generated = (
                manager_seed_0.generate_human_readable_id(o)
            )
            assert generated == h


def test_get_human_readable_id(
    filled_manager_seed_0,
    original_ids,
    human_readable_ids_seed_0
):
    for o, h in zip(original_ids, human_readable_ids_seed_0):
        assert h == filled_manager_seed_0.get_human_readable_id(o)


def test_get_original_id(
    filled_manager_seed_0,
    original_ids,
    human_readable_ids_seed_0
):
    for o, h in zip(original_ids, human_readable_ids_seed_0):
        assert o == filled_manager_seed_0.get_original_id(h)


def test_get_human_readable_id_default(
    filled_manager_seed_0,
    unused_ids,
    default_value
):
    assert filled_manager_seed_0.get_human_readable_id(
        unused_ids[0], default_value
    ) == default_value


def test_get_original_id_default(
    filled_manager_seed_0,
    unused_ids,
    default_value
):
    assert filled_manager_seed_0.get_original_id(
        unused_ids[0], default_value
    ) == default_value


def test_has_human_readable_id(
    filled_manager_seed_0,
    human_readable_ids_seed_0
):
    for h in human_readable_ids_seed_0:
        assert filled_manager_seed_0.has_human_readable_id(h)


def test_has_not_human_readable_id(
    filled_manager_seed_0,
    unused_ids
):
    for u in unused_ids:
        assert not filled_manager_seed_0.has_human_readable_id(u)


def test_has_original_id(
    filled_manager_seed_0,
    original_ids
):
    for o in original_ids:
        assert filled_manager_seed_0.has_original_id(o)


def test_has_not_original_id(
    filled_manager_seed_0,
    unused_ids
):
    for u in unused_ids:
        assert not filled_manager_seed_0.has_original_id(u)


def test_no_collision(
    manager_seed_0,
    colliding_original_ids,
    non_colliding_human_readable_ids
):
    for c, nc in zip(colliding_original_ids, non_colliding_human_readable_ids):
        assert nc == manager_seed_0.generate_human_readable_id(c)


def test_correct_len(
    filled_manager_seed_0,
    original_ids
):
    assert len(filled_manager_seed_0) == len(original_ids)
