from serial_bus.utils import convert_src_file_to


# converts src_file to YAML and saves it to a file named "yml_customers.yaml"
convert_src_file_to(src_file="customers.json", dst_format="yaml", dst_file="yml_customers.yaml")

# converts src_file to TOML and saves it to a file named "customers.toml"
convert_src_file_to(src_file="customers.json", dst_format="toml")

# raises SerialBusDumperError because the INI format doesn't support lists.
convert_src_file_to(src_file="customers.json", dst_format="ini")