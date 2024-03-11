import os
import pytest
from serial_bus.utils import convert_src_file_to
from serial_bus.config import get_config
from serial_bus.exceptions import SerialBusDumperError

# Define the supported formats
CONFIG = get_config()
# formats = CONFIG.supported_formats  #
formats = ["toml", "yaml", "yml", "ini"]


# Define a fixture for the source files
@pytest.fixture
def src_file():
    return "serial_bus/tests/mocked_data/customers.json"


# Define a fixture for the destination files
@pytest.fixture(params=formats, ids=lambda x: f"dst_format_{x}")
def dst_file(request):
    return f"serial_bus/tests/mocked_data/_customers.{request.param}"


def test_format_conversion(src_file, dst_file):
    if src_file != dst_file:
        # Convert the source file to the destination format
        dst_format = os.path.splitext(dst_file)[1].lstrip('.')
        if dst_format == 'ini':
            with pytest.raises(SerialBusDumperError):
                convert_src_file_to(src_file=src_file, dst_format=dst_format, dst_file=dst_file)
        else:
            convert_src_file_to(src_file=src_file, dst_format=dst_format, dst_file=dst_file)

            # Compare the created file with the expected file
            with open(dst_file, "r") as f_created:
                expected_file = f"serial_bus/tests/mocked_data/customers.{dst_format}"
                with open(expected_file, "r") as f_expected:
                    assert f_created.read() == f_expected.read()
