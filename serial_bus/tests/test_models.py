import os
import pytest

# Because one of the tests will need access to CustomerModel class,
# it's imported here. And because it's imported before we ever try to
# create any model instance, the `MODELS_MODULES` env var doesn't need
# to be set.
from serial_bus.tests.models import CustomerModel
from serial_bus import GLOBAL_DATA_STORE as data_store
from serial_bus.utils import generate_from_file, load_file_to_dict
from serial_bus.tests.utils import get_customer_model_records_for_assertion, get_customer_data_for_assertion


### FIXTURES ###
@pytest.fixture
def products_yaml_file():
    return "serial_bus/tests/mocked_data/products.yaml"


@pytest.fixture
def customers_json_file():
    return "serial_bus/tests/mocked_data/customers.json"


@pytest.fixture
def customers_toml_file():
    return "serial_bus/tests/mocked_data/customers.toml"


@pytest.fixture
def customers_yaml_file():
    return "serial_bus/tests/mocked_data/customers.yaml"


@pytest.fixture
def yml_customers_yaml_file():
    return "serial_bus/tests/mocked_data/yml_customers.yaml"


@pytest.fixture
def rendered_customers_txt_file():
    return "serial_bus/tests/mocked_data/rendered_customers.txt"


@pytest.fixture
def products_data(products_yaml_file):
    return load_file_to_dict(products_yaml_file)['products']


@pytest.fixture
def customers_data(customers_json_file):
    return load_file_to_dict(customers_json_file)['customers']


### TESTS ###
def test_generate_models(products_yaml_file, customers_json_file):
    # We know that all of our models module(s) have already been imported,
    # and this is enough to guarantee the 'directive_to_model_mapping' config
    # will be populated with the correct values. If that was not the case,
    # we'd have to set the 'MODELS_MODULES' env var as shown below:
    # os.environ["MODELS_MODULES"] = "serial_bus.tests.models"

    generate_from_file(products_yaml_file)
    generate_from_file(customers_json_file)


def test_ds_records_keys():
    assert len(data_store.records.keys()) == 2, "data_store.records should have exactly two keys"
    assert 'ProductModel' in data_store.records, "data_store.records should contain a key named 'ProductModel'"
    assert 'CustomerModel' in data_store.records, "data_store.records should contain a key named 'CustomerModel'"


def test_ds_records_values(products_data, customers_data):
    assert data_store.as_dict()['ProductModel'] == products_data

    _customer_records_for_assertion = get_customer_model_records_for_assertion(data_store.as_dict()['CustomerModel'])
    _customer_data = get_customer_data_for_assertion(customers_data)
    assert len(_customer_records_for_assertion) == len(_customer_data)

    for _dict in _customer_records_for_assertion:
        assert _dict in _customer_data, f"{_dict} not found in _customer_data"


def test_rendering(rendered_customers_txt_file):
    os.environ["TEMPLATES_DIR"] = "serial_bus/tests/templates"

    rendered_str = ''

    for customer in CustomerModel.get_all():
        rendered_str += f"Rendered template for customer: {customer.name}:\n"
        rendered_str += (customer.get_rendered_str() or "Customer doesn't have send_ads set to True")
        rendered_str += f"\n{'-' * 50}\n"

    with open(rendered_customers_txt_file, "r") as f:
        assert rendered_str == f.read()
