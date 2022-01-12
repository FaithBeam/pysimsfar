from unittest import TestCase

from pysimsfar.far import Far


class TestFar(TestCase):
    def setUp(self) -> None:
        self.far_file = "test.far"
        self.file_name = "test.bmp"
        self.f = Far(self.far_file)
        self.entry = self.f.manifest.manifest_entries[0]

    def test_parse_far(self):
        self.assertEqual(self.f.signature, "FAR!byAZ")
        self.assertEqual(self.f.version, 1)
        self.assertEqual(self.f.manifest_offset, 160)
        self.assertEqual(self.f.manifest.number_of_files, 1)
        self.assertEqual(len(self.f.manifest.manifest_entries), 1)
        self.assertEqual(self.f.manifest.manifest_entries[0].file_length_1, 144)
        self.assertEqual(self.f.manifest.manifest_entries[0].file_length_2, 144)
        self.assertEqual(self.f.manifest.manifest_entries[0].file_name, self.file_name)
        self.assertEqual(self.f.manifest.manifest_entries[0].file_name_length, 8)
        self.assertEqual(self.f.manifest.manifest_entries[0].file_offset, 16)

    def test_get_bytes(self):
        for e in [self.file_name, self.entry]:
            img_bytes = self.f.get_bytes(e)
            with open(self.far_file, "rb") as my_f:
                my_f.seek(16, 0)
                for i in range(144):
                    self.assertEqual(
                        int.from_bytes(my_f.read(1), "little"), img_bytes[i]
                    )
