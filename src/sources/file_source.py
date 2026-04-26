from dataclasses import dataclass
from src.contracts.task import Task
from src.errors import TaskFileNotFoundError,  InvalidTaskFormatError
from pathlib import Path

@dataclass
class FileSource:
    """Источник задач, читающий задачи из текстового файла"""
    file_path: str | Path
    def get_tasks(self) -> list[Task]:
        tasks = []
        path = Path(self.file_path)
        if not path.exists():
            raise TaskFileNotFoundError()
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.split(maxsplit=1)
            if not line or len(line) == 0:
                continue
            if len(line) < 2:
                 raise InvalidTaskFormatError()
            try:
                id_int = int(line[0])
            except ValueError:
                raise InvalidTaskFormatError()
            tasks.append(Task(id=id_int, payload=line[1]))
        return tasks