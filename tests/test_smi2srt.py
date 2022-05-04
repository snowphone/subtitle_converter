import pytest

from smi import SMI
from srt import SRT


@pytest.mark.parametrize(
    "file_path,path_expected",
    [
        (
            "tests/resource/kill_bill.euckr.smi",
            "tests/resource/kill_bill.output",
        ),
        (
            "tests/resource/spiderman.utf8.smi",
            "tests/resource/spiderman.output",
        ),
    ],
)
def test_converting(file_path: str, path_expected: str):
    frame_list = SMI(file_path).parse()
    actual = "".join(SRT(frame_list).serialize())
    with open(path_expected) as f:
        expected = f.read()

    assert expected == actual
    return
