from dataclasses import dataclass
from src.contracts.task import Task
import random

@dataclass
class GeneratorSource:
    """Источник задач, генерирующий задачи на основе заданного количества"""
    count: int
    task_examples = ["process data", "something wrong", "look at me", "tri tak tri"]
    def get_tasks(self) -> list[Task]:
        tasks = []
        for i in range(self.count):
            task_payload = self.task_examples[random.randint(0, len(self.task_examples) - 1)]
            tasks.append(Task(id=i, payload=task_payload))
        return tasks