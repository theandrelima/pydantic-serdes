# Usage

The *WHAT*s and *HOW*s of pydantic-serdes`s usage lays in the hands of the developer alone. That said, a few 
hypothetical and intentionally contrived examples might help spark some ideas.

>***NOTE**: The examples below are focused on sample code for some common use-cases. Little explanation is provided and 
> for more in-depth information on what's going on behind the scenes, check [Base Models](/docs/base_models.md)*

## Example 1: Instantiating models from serialized data

Provided the serialized YAML file with information about products in a web store, we want to be able to instantiate 
python objects that will encapsulate the same data, possibly including methods to cover certain behaviors that would 
fit the business requirements.

```yaml
# my_package/products.yaml
products:
  - prod_id: ABC123
    name: Lembas
    category: food
  - prod_id: GHI789
    name: There and Back Again
    category: books
  - prod_id: JKL012
    name: Bow & Arrows
    category: sports
  - prod_id: MNO345
    name: Mouth of Sauron - Live from The Black Gates
    category: music
  - prod_id: PQR678
    name: Eagle Flight Tickets to Mordor
    category: travel
  - prod_id: VWX234
    name: The Mazarbul-Book
    category: books
  - prod_id: YZA567
    name: Dwarfs-tossing Gloves
    category: sports
```

Knowing our data, we can create a model class that inherit from PydanticSerdesBaseModel.
> *Note the comments for some important information on special fields. More info on those can be found in [Base Models](/docs/base_models.md)*

```python
# my_package/models.py
1  from pydantic_serdes import PydanticSerdesBaseModel
2
3
4  class ProductModel(PydanticSerdesBaseModel):
5
6      _key = ("prod_id",)  # (mandatory) model fields that should be used to uniquely ID an instance.
7      _directive = "products"  # (optional) the yaml keyword that holds data for instances of this model.
8      _err_on_duplicate = True  # (optional) if data leading to duplicate instances is present, should we error?
9
10     prod_id: str
11     name: str
12     category: str
13     # Product's specific behaviors coded as methods here
14     # (...)
```

With the data modeling done, we only need to load our models up.

```python
1 import os
2 from pydantic_serdes.utils import generate_from_file
3 
4 if __name__ == "__main__":
5     # this makes sure pydantic_serdes will know where to look for model classes.
6     # if your model classes are scattered through more than one module, make it a CSV str.
7     os.environ["MODELS_MODULES"] = "my_package.models"
8 
9     # all the heavy-lifting happens seamlessly.
10    generate_from_file("products.yaml")
```

Except for the imports and the "*main* guard" we didn't have to do a lot to get instances of our CustomerModel. Let's 
break down what's going on here:

- line 7 sets the `MODELS_MODULES` environment variable which is an explicit way of informing pydantic-serdes 
  of where to look to find model classes that inherit from **PydanticSerdesBaseModel**. There is an 
  implicit way of doing the same explained in [Configuration & Extensibility](docs/configuration--extensibility.md). 
  ***Also, it's worth noting that this is typically something you would ensure to be set in your environment before the 
  code runs. It was done like this here for the sake of the example.***
- line 10 is where all the magic happens. It simply invokes `generate_from_file`, passing a string pointing to our 
  serialized data file path. From a developer's perspective, this function encapsulates all the required logic to:
  1. automatically identify a proper loader function and load the data from the file into a python data structure;
  2. discover which model class(es) to use to instantiate objects from the loaded data;
  3. store those instantiated objects in a cached datastructure globally accessible *(we will see it next)*

The last item above might not be so obvious, since it always happens automatically whenever a new model object is 
instantiated. So let's make it crystal clear now. For the below snippet, imagine we are editing from line 11 of the 
same `my_package/main.py` file.

```python
# my_package/main.py
11  import json
12
13  from pydantic_serdes import GLOBAL_DATA_STORE as datastore
14
15  print(datastore.records)
16  print(json.dumps(datastore.as_dict(), indent=4))
```

As you might gather from the above code, [GLOBAL_DATA_STORE](/docs/the_global_data_store.md) is an object that holds 
a `.records` property returning a data structure (defaultdict) with all our model instances. pydantic-serdes takes care of 
automatically storing new model instances in the `GLOBAL_DATA_STORE` as they get created (*more info in 
[PydanticSerdesBaseModel](/docs/base_models.md#PydanticSerdesBaseModel)*)

We can see the contents of that defaultdict with the print statement from line 15:
```bash
defaultdict(<class 'pydantic_serdes.custom_collections.PydanticSerdesSortedSet'>, {'ProductModel': PydanticSerdesSortedSet([ProductModel(prod_id='ABC123',
name='Lembas', category='food'), ProductModel(prod_id='GHI789', name='There and Back Again', category='books'), ProductModel(prod_id='JKL012', name='Bow & Arrows',
category='sports'), ProductModel(prod_id='MNO345', name='Mouth of Sauron - Live from The Black Gates', category='music'), ProductModel(prod_id='PQR678', name='Eagle
Flight Tickets to Mordor', category='travel'), ProductModel(prod_id='VWX234', name='The Mazarbul-Book', category='books'), ProductModel(prod_id='YZA567',
name='Dwarfs-tossing Gloves', category='sports')], key=<function PydanticSerdesSortedSet.__init__.<locals>.<lambda> at 0x7fabd0e331f0>)})
```

Defaultdicts are awesome, but not very readable. The `GLOBAL_DATA_STORE` object also has a `.as_dict()` method which 
returns a regular dictionary with the same data found in the `.records` property, and that can be prettier printed using
`json.dumps()` returned string, as we did in line 16:
```bash
{
    "ProductModel": [
        {
            "prod_id": "ABC123",
            "name": "Lembas",
            "category": "food"
        },
        {
            "prod_id": "GHI789",
            "name": "There and Back Again",
            "category": "books"
        },
        {
            "prod_id": "JKL012",
            "name": "Bow & Arrows",
            "category": "sports"
        },
        {
            "prod_id": "MNO345",
            "name": "Mouth of Sauron - Live from The Black Gates",
            "category": "music"
        },
        {
            "prod_id": "PQR678",
            "name": "Eagle Flight Tickets to Mordor",
            "category": "travel"
        },
        {
            "prod_id": "VWX234",
            "name": "The Mazarbul-Book",
            "category": "books"
        },
        {
            "prod_id": "YZA567",
            "name": "Dwarfs-tossing Gloves",
            "category": "sports"
        }
    ]
}
```

Just to make sure it's clear:
  - to access your model instances, use `GLOBAL_DATA_STORE.records`;
  - for a regular dict representation of all your models (not the actual model instances), then 
    `GLOBAL_DATA_STORE.as_dict()`;

***

## Example 2: Data Relationship & Model Rendering

Let's expand on Example 1 and throw customer data in the mix. To make things even a little more interesting (and to 
prove the point that pydantic-serdes can work seamlessly with multiple serialization formats), let's make it 
through a separate *.json* file now:

```json
# my_package/customers.json
{
    "customers": [
        {
            "name": "John Doe",
            "age": 25,
            "email": "john.doe@example.com",
            "send_ads": true,
            "flagged_interests": [
                "sports",
                "music"
            ]
        },
        {
            "name": "Jane Smith",
            "age": 30,
            "email": "jane.smith@example.com",
            "send_ads": false,
            "flagged_interests": [
                "books"
            ]
        },
        {
            "name": "Alice Johnson",
            "age": 35,
            "email": "alice.johnson@example.com",
            "send_ads": true,
            "flagged_interests": [
                "travel",
                "food"
            ]
        }
    ]
}
```

The field `flagged_interests` creates a relationship between products and customers, meaning that in our 
`CustomerModel`, we will need to have a field that stores that 1:N relationship. Because a 
`PydanticSerdesBaseModel` class implements `__hashable__`, we have to do that by using a tuple object, since it is 
python's only built-in hashable sequence type. You could use any other custom hashable sequence type you 
might want to.

Also, we want to fill-up this tuple field with ProductModel instances, and not simply strings, which means that part 
of the efforts of creating a ProductModel will include queries to our `GLOBAL_DATA_STORE` for ProductModel instances 
matching a certain criteria.

Finally, we want to use the data in CustomerModel to easily build a marketing message about products that are 
related to a customer interests. This is something we can easily achieve by using the concept of renderable models, 
employing jinja templates to the task.

We will continue to edit from line 16 in the same my_package/models.py file, but first we import what we need from 
lines 2 to 4

```python
# my_package/models.py
1  from pydantic_serdes import PydanticSerdesBaseModel
2  from pydantic_serdes import PydanticSerdesRenderableModel
3  from pydantic import EmailStr, Field
4  from typing import Tuple
5
6  class ProductModel:
7  # (...) same as before

21  class CustomerModel(PydanticSerdesRenderableModel):  # PydanticSerdesRenderableModel is also a child class of PydanticSerdesBaseModel)
22      _key = ("email",)
23      _directive = "customers"
24      _err_on_duplicate = True
25      
26      name: str
27      age: int = Field(ge=18, le=100)
28      email: EmailStr
29      flagged_interests: Tuple[ProductModel, ...]
30      
31      @ classmethod
32      def create(cls, dict_args, *args, **kwargs):
33          interests = list()
34          for category in dict_args["flagged_interests"]:
35              interests += [prod for prod in ProductModel.filter({"category": category})]
36          # pydantic_serdes will take care of ultimately converting this to a tuple.
37          dict_args["flagged_interests"] = interests
38          super().create(dict_args, *args, **kwargs)
39
40      # here come other methods for CustomerModel (...)
```

Before anything else, it's important to say that `PydanticSerdesRenderableModel` also inherits from 
`PydanticSerdesBaseModel`. It merely extends it to include a template rendering functionality as we will see below.

Now, let's focus on what's new here:
- line 25 set the `flagged_interests` field to a Tuple of `ProductModel` instances. This is where the relationship 
  between the two models will exist.
- To make sure we achieve that, line 28 overwrites the `create()` class method, which is a factory method that 
  expects to receive a dictionary containing key:value pairs loaded from the serialized data. Inside this method we:
  1. create an empty `interests` list that will be filled with ProductModel objects;
  2. for each *category* string in `flagged_interest`, we find all `ProducModel` instances that has the "category" 
     field matching it and put each inside the `interests` list created before.
  3. after looping all categories and having our `interests` list assembled, we assign it as the new value for the 
     `flagged_interests` key of dict_args
  4. finally, we call for the super class `.create()` method passing the transformed dict_args.

> OBS: this could have easily been done using comprehension, but the standard for loop makes the steps more explicit.

About step ii above, two things are worth noting:  
  1 - The query to our `GLOBAL_DATA_STORE` was actually carried out by the `.filter()` method that any child class 
of `PydanticSerdesBaseModel` will have. This method basically accepts a dictionary with one k:v pair that will 
be used for the query. ***NOTE:** currently the query supports only one k:v pair.* For other querying options, 
refer to [PydanticSerdesBaseModel docs](/docs/base_models.md#PydanticSerdesbasemodel).  
  2 - even though we used a list object, child classes of `PydanticSerdesBaseModel` are prepared to automatically 
type cast an argument received as a list that is expected by a field of type Tuple.

Finally, with our model ready to go, we just need to add another call to `.generate_from_file()` method in 
my_package/main.py, but now passing our `customers.json` file as the argument. Below, we edit the file to look like 
this:

```python
# my_package/main.py
1  import os
2  import json
3  from pydantic_serdes import GLOBAL_DATA_STORE as datastore
4  from pydantic_serdes.utils import generate_from_file
5
6  if __name__ == "__main__":
7    # this makes sure pydantic_serdes will know where to look for model classes.
8    # if your model classes are scattered through more than on module, make it a CSV str.
9    os.environ["MODELS_MODULES"] = "my_package.models"
10
11   # all the heavy-lifting happens here seamlessly.
12   generate_from_file("products.yaml")
13   generate_from_file("customers.json")
14
15   print(datastore.records)
16   print(json.dumps(datastore.as_dict(), indent=4)) 
```

Below is the output for line 16 only:

```bash
{
    "ProductModel": [...], # same as before
    "CustomerModel": [
        {
            "name": "Alice Johnson",
            "age": 35,
            "email": "alice.johnson@example.com",
            "flagged_interests": [
                {
                    "prod_id": "PQR678",
                    "name": "Eagle Flight Tickets to Mordor",
                    "category": "travel"
                },
                {
                    "prod_id": "ABC123",
                    "name": "Lembas",
                    "category": "food"
                }
            ]
        },
        {
            "name": "Jane Smith",
            "age": 30,
            "email": "jane.smith@example.com",
            "flagged_interests": [
                {
                    "prod_id": "GHI789",
                    "name": "There and Back Again",
                    "category": "books"
                },
                {
                    "prod_id": "VWX234",
                    "name": "The Mazarbul-Book",
                    "category": "books"
                }
            ]
        },
        {
            "name": "John Doe",
            "age": 25,
            "email": "john.doe@example.com",
            "flagged_interests": [
                {
                    "prod_id": "JKL012",
                    "name": "Bow & Arrows",
                    "category": "sports"
                },
                {
                    "prod_id": "YZA567",
                    "name": "Dwarfs-tossing Gloves",
                    "category": "sports"
                },
                {
                    "prod_id": "MNO345",
                    "name": "Mouth of Sauron - Live from The Black Gates",
                    "category": "music"
                }
            ]
        }
    ]
}
```

**About the templating logic:** A `PydanticSerdesRenderableModel` class by default expects to find a Jinja2 
template file under a default location with a default name (if none is given). For detailed information about these 
defaults, refer to [PydanticSerdesRenderableModel](/docs/base_models.md#PydanticSerdesrenderablemodel).

In our case here all those defaults would lead our instances to expect to find the following jinja2 template file to 
use when rendering their data into templates: `./templates/customer.j2`.

```jinja
# my_package/templates/customer.j2
{% if send_ads %}
Dear {{ name | capitalize }},
We'd like to let you know that we recently added the following products to our store that we think you might like:
{% for product in flagged_interests -%}
    - {{ product.name }}
{% endfor %}
We hope you find something you like!

OBS: You are receiving this message in {{ email }} because you are registered for receiving ads
{% endif %}
```

To get the rendered string returned by the template, we only need to call the `.get_rendered_str()` method from a 
`PydanticSerdesRenderableModel`.

For example:
```python
for customer in CustomerModel.get_all():
    print(f"Rendered template for customer: {customer.name}:")
    print(customer.get_rendered_str() or "Customer doesn't have send_ads set to True")
    print("-" * 50)
```
Output:
```bash
Rendered template for customer: Alice Johnson:

Dear Alice johnson,
We'd like to let you know that we recently added the following products to our store that we think you might like:
- Eagle Flight Tickets to Mordor
- Lembas

We hope you find something you like!

OBS: You are receiving this message in alice.johnson@example.com because you are registered for receiving ads

--------------------------------------------------
Rendered template for customer: Jane Smith:
Customer doesn't have send_ads set to True
--------------------------------------------------
Rendered template for customer: John Doe:

Dear John doe,
We'd like to let you know that we recently added the following products to our store that we think you might like:
- Bow & Arrows
- Dwarfs-tossing Gloves
- Mouth of Sauron - Live from The Black Gates

We hope you find something you like!

OBS: You are receiving this message in john.doe@example.com because you are registered for receiving ads
```

***

## Example 3: Converting data between supported formats

A nice side effect of the features included with pydantic-serdes, is that it can be used as an effective tool 
for easily converting serialized data between any two supported formats, as long as the data types from the source 
serialization format are also supported by the destination format.

Let's use the `customers.json` file we created in Example 2 above. The following code shows how easily it would be 
to generate files of other formats:

```python
1   from pydantic_serdes.utils import convert_src_file_to
2
3   # converts src_file to YAML and saves it to a file named "yml_customers.yaml"
4   convert_src_file_to(src_file="customers.json", dst_format="yaml", dst_file="yml_customers.yaml")
5
6   # converts src_file to TOML and saves it to a file named "customers.toml"
7   convert_src_file_to(src_file="customers.json", dst_format="toml")
8
9   # raises PydanticSerdesDumperError because the INI format doesn't support lists.
10  convert_src_file_to(src_file="customers.json", dst_format="ini")
```

The `convert_src_file_to` function needs only to know: 
- src_file: path to a source file (either a string or a Path object)
- dst_format: the format you intend to convert data to
- dst_file: optional argument to explicitly give the resulting file a name. If not informed, it will take the exact 
  same name of the `src_file`, but now with a suffix matching dst_format.

Notice that for this use-case of simply converting from one format to another, there's no real need to have a model 
defined. 

As it was the case when loading serialized data from a file into models, we don't really need to tell 
pydantic-serdes what's the serialization format of the source file, as it will automatically infer by the file 
suffix itself. So make sure your source file adheres to the well-known
file extensions:
- YAML: .yaml or .yml
- JSON: .json
- INI: .ini
- TOML: .toml