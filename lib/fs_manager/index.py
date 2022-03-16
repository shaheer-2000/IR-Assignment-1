from pathlib import Path
from pickle import dump as pdump, load as pload, HIGHEST_PROTOCOL as P_HIGHEST_PROTOCOL


class FSManager:
    def __init__(self):
        pass

    @staticmethod
    def get_files_in_dir(dir_path, rename_file_cb=lambda f: f):
        target_dir = Path(dir_path).resolve()

        if not target_dir.exists():
            raise NotADirectoryError()

        return [rename_file_cb(file.name) for file in target_dir.iterdir() if file.is_file()]

    @staticmethod
    def rmdir(target_dir: Path):
        if not target_dir.exists():
            raise NotADirectoryError()

        for child in target_dir.iterdir():
            if child.is_file():
                child.unlink()
            else:
                FSManager.rmdir(child)

        target_dir.rmdir()

    @staticmethod
    def mkdir(dir_path: str, delete_if_exists=False):
        target_dir = Path(dir_path).resolve()

        if delete_if_exists:
            FSManager.rmdir(target_dir)
        else:
            if target_dir.exists():
                # can silent kill exceptions if need be; keeping for now
                raise FileExistsError()

        target_dir.mkdir(parents=True)

    @staticmethod
    def resolve_path(p: str):
        return str(Path(p).resolve())

    @staticmethod
    def write_file(file_path, content):
        target_file = Path(file_path).resolve()

        with target_file.open(mode="w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def read_file(file_path):
        target_file = Path(file_path).resolve()

        content = None
        try:
            with target_file.open(mode="r") as f:
                content = f.read()
        except UnicodeDecodeError:
            print(file_path)

        return content

    @staticmethod
    def pickle_struct(file_path=None, struct=None):
        if type(file_path) is not str or not file_path.endswith('.pickle') or struct is None:
            raise ValueError()

        target_file = Path(file_path).resolve()

        if target_file.exists():
            if not target_file.is_file():
                raise IsADirectoryError()

            target_file.unlink()
        else:
            FSManager.mkdir(str(target_file.parents[0]))

        with target_file.open(mode="wb") as f:
            pdump(struct, f, P_HIGHEST_PROTOCOL)

    @staticmethod
    def unpickle_struct(file_path=None):
        if type(file_path) is not str or not file_path.endswith('.pickle'):
            raise ValueError()

        target_file = Path(file_path).resolve()

        if not target_file.exists():
            raise FileExistsError()

        if not target_file.is_file():
            raise IsADirectoryError()

        with target_file.open(mode="rb") as f:
            data = pload(f)

        return data
