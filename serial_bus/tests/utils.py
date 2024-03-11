"""
This module contains utility functions for test cases
"""


def sort_lists_in_dict(d):
    for k, v in d.items():
        if isinstance(v, list):
            v.sort()

        elif isinstance(v, dict):
            sort_lists_in_dict(v)


def get_customer_model_records_for_assertion(customer_model_records):
    for customer_dict in customer_model_records:
        customer_dict["flagged_interests"] = list(
            {interest['category'] for interest in customer_dict["flagged_interests"]})
        sort_lists_in_dict(customer_dict)

    return customer_model_records


def get_customer_data_for_assertion(customers_data):
    for c_data in customers_data:
        sort_lists_in_dict(c_data)

    return customers_data
