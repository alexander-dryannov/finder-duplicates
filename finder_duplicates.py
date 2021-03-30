import os
import sys
import time
import hashlib
from pathlib import Path
from tqdm import tqdm


class FinderDuplicates:
    def __init__(self, path_from_where, path_where):
        self.path_from_where = Path(path_from_where)
        self.path_where = Path(path_where)
        self._list_file_paths = self._getting_file_paths()
        self._hashes = self._get_hashes_from_files(self._list_file_paths)

    """Получаю пути до файлов"""
    def _getting_file_paths(self):
        file_extension_filters = ['jpg', 'JPG', 'png', 'PNG']
        list_file_paths = []
        for path in self.path_from_where.iterdir():
            if path.is_file() and (str(path).partition('.')[-1] != i for i in file_extension_filters):

                list_file_paths.append(str(path))
        return list_file_paths

    @staticmethod
    def _create_folder(path):
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

    """Собираю хэши"""
    @staticmethod
    def _get_hashes_from_files(files):
        hashes = {}
        for i in tqdm(files):
            try:
                with open(i, 'rb') as f:
                    hashes[i] = hashlib.sha224(f.read()).hexdigest()
            except IsADirectoryError:
                continue
        return hashes

    """Ищу дубликаты"""
    def find_duplicate(self):
        reverse_dict = {}
        self._create_folder(self.path_where)
        for key, value in self._hashes.items():
            try:
                reverse_dict[value].append(key)
            except KeyError:
                reverse_dict[value] = [key]
        for item in list(reverse_dict.values()):
            if len(item) > 1:
                for sub_item in tqdm(item[1:], leave=False):
                    Path(sub_item).rename(Path(str(self.path_where) + '/' + sub_item.split("/")[-1]))


if __name__ == '__main__':
    print('Поехали!')
    start_time = time.monotonic()
    FinderDuplicates(sys.argv[2], sys.argv[4]).find_duplicate()
    print(f'Завершено. Затрачено времени: {(time.monotonic() - start_time):.3f}')
