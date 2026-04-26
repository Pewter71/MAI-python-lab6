"""
CLI и получение задач из разных источников
"""
from src.sources.wrong_source import WrongSource
from src.sources.generator_source import GeneratorSource
from src.sources.file_source import FileSource
from src.sources.json_source import JsonSource
from src.receiver import receive_tasks

def main():
    while True:
        print("\nВыберите источник задач:")
        print("1. Файл JSONL")
        print("2. Генератор")
        print("3. Файл txt")
        print("4. Неправильный источник")
        print("0. Выход")
        
        choice = input("Введите номер источника: ").strip()
        if choice == "1":
            source = JsonSource(path="file_sources/jsonl_source.jsonl")
        elif choice == "2":
            source = GeneratorSource(count=5)
        elif choice == "3":
            source = FileSource(file_path="file_sources/file_source1.txt")
        elif choice == "4":
            source = WrongSource()
        elif choice == "0":
            print("Выход из программы")
            break
        else:
            print("Введите число из списка!")
            continue
        try:
            tasks = receive_tasks(source)
            print(f"Получено {len(tasks)} задач:")
            for task in tasks:
                print(f"id: {task.id}, payload: {task.payload}")
        except Exception as e:
            print(f"Ошибка при получении задач: {e}")


if __name__ == "__main__":
    main()