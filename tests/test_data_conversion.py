import os

import pytest

from pydantic_serdes.config import get_config
from pydantic_serdes.exceptions import PydanticSerdesDumperError
from pydantic_serdes.utils import convert_src_file_to

# Define the supported formats
CONFIG = get_config()
# formats = CONFIG.supported_formats  #
formats = ["toml", "yaml", "yml", "ini"]


# Define a fixture for the source files
@pytest.fixture
def src_file():
    return "tests/mocked_data/customers.json"


# Define a fixture for the destination files
@pytest.fixture(params=formats, ids=lambda x: f"dst_format_{x}")
def dst_file(request):
    return f"tests/mocked_data/_customers.{request.param}"


def test_format_conversion(src_file, dst_file):
    if src_file != dst_file:
        # Convert the source file to the destination format
        dst_format = os.path.splitext(dst_file)[1].lstrip(".")
        if dst_format == "ini":
            with pytest.raises(PydanticSerdesDumperError):
                convert_src_file_to(
                    src_file=src_file, dst_format=dst_format, dst_file=dst_file
                )
        else:
            convert_src_file_to(
                src_file=src_file, dst_format=dst_format, dst_file=dst_file
            )

            # Compare the created file with the expected file
            with open(dst_file, "r") as f_created:
                expected_file = f"tests/mocked_data/customers.{dst_format}"
                with open(expected_file, "r") as f_expected:
                    assert f_created.read() == f_expected.read()
