"""
Тесты для класса FileSource
"""
import pytest
from pathlib import Path
from src.sources.file_source import FileSource
from src.contracts.task_source import TaskSource
from src.errors import TaskFileNotFoundError



def test_file_source_implements_protocol():
    """Тест того, что FileSource реализует протокол TaskSource"""
    source = FileSource(file_path="some_path.txt")
    assert isinstance(source, TaskSource)


def test_file_source_read_basic(tmp_path):
    """Тест чтения обычного файла с задачами"""
    path = tmp_path / "tasks.txt"
    path.write_text("1 first task\n2 second task\n", encoding="utf-8")

    tasks = FileSource(file_path=str(path)).get_tasks()

    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[0].payload == "first task"
    assert tasks[1].id == 2
    assert tasks[1].payload == "second task"


def test_file_source_empty_file(tmp_path):
    """Тест чтения пустого файла"""
    path = tmp_path / "empty.txt"
    path.write_text("", encoding="utf-8")

    tasks = FileSource(file_path=str(path)).get_tasks()
    assert tasks == []


def test_file_source_skip_empty_lines(tmp_path):
    """Тест пропуска пустых строк"""
    path = tmp_path / "with_blanks.txt"
    path.write_text("1 alpha\n\n\n2 beta\n\n", encoding="utf-8")

    tasks = FileSource(file_path=str(path)).get_tasks()
    assert len(tasks) == 2
    assert tasks[0].payload == "alpha"
    assert tasks[1].payload == "beta"


def test_file_source_file_not_found():
    """Тест отсутствующего файла"""
    source = FileSource(file_path="does_not_exist_12345.txt")
    with pytest.raises(TaskFileNotFoundError):
        source.get_tasks()

