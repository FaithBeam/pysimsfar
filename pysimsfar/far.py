from typing import Optional


class ManifestEntryNotFoundError(Exception):
    """Raise for manifest entry not found exception."""


class Far:
    def __init__(self, path_to_far):
        self._path_to_far = path_to_far
        self.signature: Optional[str]
        self.version: Optional[int]
        self.manifest_offset: Optional[int] = None
        self.manifest: Optional[Manifest] = None

        self.__parse_far()

    def __parse_far(self):
        with open(self._path_to_far, "rb") as f:
            self.signature = f.read(8).decode()
            self.version = int.from_bytes(f.read(4), "little")
            self.manifest_offset = int.from_bytes(f.read(4), "little")
            f.seek(self.manifest_offset, 0)
            self.manifest = Manifest()
            self.manifest.number_of_files = int.from_bytes(f.read(4), "little")

            for i in range(self.manifest.number_of_files):
                self.manifest.manifest_entries.append(self.__parse_manifest_entry(f))

    @staticmethod
    def __parse_manifest_entry(f):
        manifest_entry = ManifestEntry()
        manifest_entry.file_length_1 = int.from_bytes(f.read(4), "little")
        manifest_entry.file_length_2 = int.from_bytes(f.read(4), "little")
        manifest_entry.file_offset = int.from_bytes(f.read(4), "little")
        manifest_entry.file_name_length = int.from_bytes(f.read(4), "little")
        manifest_entry.file_name = f.read(manifest_entry.file_name_length).decode()
        return manifest_entry

    def get_bytes(self, entry):
        if type(entry) is str:
            try:
                for e in self.manifest.manifest_entries:
                    if e.file_name == entry:
                        entry = e
                        break
                else:
                    raise ManifestEntryNotFoundError
            except ManifestEntryNotFoundError:
                print(f"Entry {entry} not found.")
        with open(self._path_to_far, "rb") as f:
            f.seek(entry.file_offset, 0)
            return f.read(entry.file_length_1)


class Manifest:
    def __init__(self):
        self.number_of_files: Optional[int] = None
        self.manifest_entries: Optional[list[ManifestEntry]] = []


class ManifestEntry:
    def __init__(self):
        self.file_length_1: Optional[int] = None
        self.file_length_2: Optional[int] = None
        self.file_offset: Optional[int] = None
        self.file_name_length: Optional[int] = None
        self.file_name: Optional[str] = None
