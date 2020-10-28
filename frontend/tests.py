"""Tests for the frontend app."""

import pytest
from hypothesis import example, given
from hypothesis.strategies import text


@pytest.mark.django_db
class TestNothing:
    """Do nothing."""

    do_nothing: bool = True

    @given(string=text())
    @example(string='Not doing anything')
    def test_nothing(self, string: str):
        """Testnothing."""
        assert self.do_nothing
