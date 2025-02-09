from typing import Any

import pytest

from source.settings import validate_settings


def test_empty_key(monkeypatch: Any, capsys: Any) -> None:
    monkeypatch.delenv("OPENAI_API_KEY")

    with pytest.raises(SystemExit):
        validate_settings()

    output = capsys.readouterr()

    assert "OPENAI_API_KEY is not set, please check your settings" in output.err
