"""
Тесты для класса JsonSource
"""
import pytest
from pathlib import Path
from src.sources.json_source import JsonSource
from src.contracts.task_source import TaskSource
from src.errors import (
    TaskFileNotFoundError,
    InvalidTaskFormatError,
    MissingTaskFieldError,
)


def test_json_source_protocol():
    """Тест того, что JsonSource реализует протокол TaskSource"""
    source = JsonSource(path="some_path.jsonl")
    assert isinstance(source, TaskSource)


def test_json_source_read_basic(tmp_path):
    """Тест чтения обычного JSONL файла"""
    path = tmp_path / "tasks.jsonl"
    path.write_text(
        '{"id": "1", "payload": "first"}\n'
        '{"id": "2", "payload": "second"}\n',
        encoding="utf-8",
    )
    tasks = JsonSource(path=str(path)).get_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[0].payload == "first"
    assert tasks[1].id == 2
    assert tasks[1].payload == "second"


def test_json_source_empty_file(tmp_path):
    """Тест чтения пустого JSONL файла"""
    path = tmp_path / "empty.jsonl"
    path.write_text("", encoding="utf-8")
    tasks = JsonSource(path=str(path)).get_tasks()
    assert tasks == []



def test_json_source_file_not_found():
    """Тест отсутствующего файла"""
    source = JsonSource(path="does_not_exist_12345.jsonl")
    with pytest.raises(TaskFileNotFoundError):
        source.get_tasks()


def test_json_source_invalid_json(tmp_path):
    """Тест некорректной JSON строки"""
    path = tmp_path / "broken.jsonl"
    path.write_text('{"id": "1", "payload":\n', encoding="utf-8")

    with pytest.raises(InvalidTaskFormatError):
        JsonSource(path=str(path)).get_tasks()


def test_json_source_missing_id(tmp_path):
    """Тест отсутствия поля id"""
    path = tmp_path / "no_id.jsonl"
    path.write_text('{"payload": "no id here"}\n', encoding="utf-8")
    with pytest.raises(MissingTaskFieldError):
        JsonSource(path=str(path)).get_tasks()


def test_json_source_missing_payload(tmp_path):
    """Тест отсутствия поля payload"""
    path = tmp_path / "no_payload.jsonl"
    path.write_text('{"id": "1"}\n', encoding="utf-8")

    with pytest.raises(MissingTaskFieldError):
        JsonSource(path=str(path)).get_tasks()


