"""Tests the finding capabilites"""
import pytest

from conda_suggest.generate import generate_map, DEFAULT_REMOVE_EXPRS


BASIC_CACHE = {
    "2dfatmic-1.0-he991be0_0.tar.bz2": {
        "executables": ["2dfatmic"],
        "package": "2dfatmic",
    },
    "cysignals-1.4.0-py36_1.tar.bz2": {
        "executables": ["__pycache__", "cysignals-CSI", "cysignals-CSI-helper.py"],
        "package": "cysignals",
    },
    "django-1.10-py34_0.tar.bz2": {
        "executables": ["__pycache__", "django-admin", "django-admin.py"],
        "package": "django",
    },
    "yt-3.6.0-py36h785e9b2_1.tar.bz2": {"executables": ["iyt", "yt"], "package": "yt"},
    "zict-0.0.3-py35_0.tar.bz2": {"executables": [], "package": "zict"},
}


@pytest.mark.parametrize(
    "remove_exprs,exp",
    [
        (
            (),
            """
2dfatmic:2dfatmic
__pycache__:cysignals
__pycache__:django
cysignals-CSI:cysignals
cysignals-CSI-helper.py:cysignals
django-admin:django
django-admin.py:django
iyt:yt
yt:yt
""",
        ),
        (
            DEFAULT_REMOVE_EXPRS,
            """
2dfatmic:2dfatmic
cysignals-CSI:cysignals
cysignals-CSI-helper.py:cysignals
django-admin:django
django-admin.py:django
iyt:yt
yt:yt
""",
        ),
        (
            ("__pycache__", ".*yt"),
            """
2dfatmic:2dfatmic
cysignals-CSI:cysignals
cysignals-CSI-helper.py:cysignals
django-admin:django
django-admin.py:django
""",
        ),
        ((".*",), ""),
    ],
)
def test_generate_map_remove_exprs(remove_exprs, exp, tmpdir):
    obs = generate_map(
        BASIC_CACHE, "test", "linux-64", remove_exprs=remove_exprs, write=False
    )
    assert exp.lstrip() == obs
