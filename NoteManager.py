import json
import os
from datetime import datetime


class Note:
    def __init__(self, id, title, body, created_at, updated_at):
        self.id = id
        self.title = title
        self.body = body
        self.created_at = created_at
        self.updated_at = updated_at

class NoteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = []

    def load_notes(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                for note_data in data:
                    note = Note(
                        note_data['id'],
                        note_data['title'],
                        note_data['body'],
                        note_data['created_at'],
                        note_data['updated_at']
                    )
                    self.notes.append(note)

    def save_notes(self):
        data = []
        for note in self.notes:
            data.append({
                'id': note.id,
                'title': note.title,
                'body': note.body,
                'created_at': note.created_at,
                'updated_at': note.updated_at
            })
        with open(self.file_path, 'w') as file:
            json.dump(data, file)

    def add_note(self, title, body):
        id = len(self.notes) + 1
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_at = created_at
        note = Note(id, title, body, created_at, updated_at)
        self.notes.append(note)
        self.save_notes()

    def edit_note(self, id, title, body):
        for note in self.notes:
            if note.id == id:
                note.title = title
                note.body = body
                note.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_notes()
                return True
        return False

    def delete_note(self, id):
        for note in self.notes:
            if note.id == id:
                self.notes.remove(note)
                self.save_notes()
                return True
        return False

    def get_note_by_id(self, id):
        for note in self.notes:
            if note.id == id:
                return note
        return None

    def get_all_notes(self):
        return self.notes


def main():
    file_path = 'notes.json'
    note_manager = NoteManager(file_path)
    note_manager.load_notes()

    while True:
        print('1. Создать заметку')
        print('2. Просмотреть список заметок')
        print('3. Редактировать заметку')
        print('4. Удалить заметку')
        print('5. Выйти')

        choice = input('Выберите действие: ')

        if choice == '1':
            title = input('Введите заголовок заметки: ')
            body = input('Введите текст заметки: ')
            note_manager.add_note(title, body)
            print('Дело сделано! Заметка создана!')

        elif choice == '2':
            notes = note_manager.get_all_notes()
            for note in notes:
                print(f'ID: {note.id}')
                print(f'Заголовок: {note.title}')
                print(f'Текст: {note.body}')
                print(f'Дата создания: {note.created_at}')
                print(f'Дата последнего изменения: {note.updated_at}')
                print('---')

        elif choice == '3':
            id = int(input('Введите ID заметки для редактирования: '))
            note = note_manager.get_note_by_id(id)
            if note:
                title = input('Введите новый заголовок заметки: ')
                body = input('Введите новый текст заметки: ')
                if note_manager.edit_note(id, title, body):
                    print('Дело сделано! Заметка успешно отредактирована!')
                else:
                    print('Ты меня с кем-то путаешь! Заметка с указанным ID не найдена.')
            else:
                print('Ты меня с кем-то путаешь! Заметка с указанным ID не найдена.')

        elif choice == '4':
            id = int(input('Введите ID заметки для удаления: '))
            if note_manager.delete_note(id):
                print('Дело сделано! Заметка успешно удалена!')
            else:
                print('Ты меня с кем-то путаешь! Заметка с указанным ID не найдена.')

        elif choice == '5':
            break

        print()

    note_manager.save_notes()


if __name__ == '__main__':
    main()