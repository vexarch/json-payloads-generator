# JSONGenerator Documentation

A powerful, flexible Python class for generating realistic JSON test data with rule-based placeholders and customizable schemas.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Schema Definition](#schema-definition)
- [Rule System](#rule-system)
- [Built-in Rules](#built-in-rules)
- [Custom Rules](#custom-rules)
- [File-based Data](#file-based-data)
- [API Reference](#api-reference)
- [Advanced Examples](#advanced-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The `JSONGenerator` class provides a comprehensive solution for generating realistic JSON test data. It supports:

- **Schema-driven generation** with type definitions and validation
- **Rule-based value generation** with built-in and custom rules
- **Placeholder patterns** for flexible value customization
- **File-based data loading** for realistic datasets
- **Unique value tracking** to prevent duplicates
- **Nested objects and arrays** for complex data structures
- **Multiple output formats** (JSON strings or Python objects)

## Installation

Simply include the `JSONGenerator` class in your Python project. The class uses only standard library modules:

```python
import json
import random
import string
import uuid
import datetime
from typing import Any, Dict, List, Union, Callable, Optional
from pathlib import Path
import re
```

## Quick Start

```python
from json_generator import JSONGenerator

# Create generator instance
generator = JSONGenerator()

# Define simple schema
schema = {
    "id": {"type": "int", "rule": "@{6}unique"},
    "name": {"type": "str", "rule": "name"},
    "email": {"type": "str", "rule": "email"},
    "age": {"type": "int", "rule": "@{18-65}range"}
}

# Set schema and generate data
generator.set_schema(schema)
users = generator.generate(5, as_string=False)

for user in users:
    print(json.dumps(user, indent=2))
```

## Schema Definition

### Basic Schema Structure

A schema is a dictionary where each key represents a JSON field with configuration:

```python
schema = {
    "field_name": {
        "type": "data_type",     # Required: int, float, double, bool, str, array, object
        "rule": "generation_rule" # Optional: how to generate the value
    }
}
```

### Supported Data Types

| Type | Description | Example |
|------|-------------|---------|
| `int` | Integer numbers | `42` |
| `float` | Floating-point numbers | `3.14` |
| `double` | Double precision (same as float) | `99.99` |
| `bool` | Boolean values | `true` or `false` |
| `str` | String values | `"hello world"` |
| `array` | Arrays of items | `[1, 2, 3]` |
| `object` | Nested objects | `{"key": "value"}` |

### Array Configuration

```python
{
    "tags": {
        "type": "array",
        "items": {
            "type": "str",
            "rule": "@{tag1,tag2,tag3}choice"
        },
        "length": 3  # Fixed length or random if omitted
    }
}
```

### Object Configuration

```python
{
    "profile": {
        "type": "object",
        "properties": {
            "bio": {"type": "str", "rule": "description"},
            "score": {"type": "int", "rule": "@{0-100}range"},
            "settings": {
                "type": "object",
                "properties": {
                    "theme": {"type": "str", "rule": "@{light,dark}choice"},
                    "notifications": {"type": "bool", "rule": "bool"}
                }
            }
        }
    }
}
```

## Rule System

### Rule Types

#### 1. Built-in Rules
Simple rule names that use predefined generators:
```python
{"type": "str", "rule": "email"}      # Generates email addresses
{"type": "str", "rule": "username"}   # Generates usernames
{"type": "int", "rule": "age"}        # Generates ages
```

#### 2. Pattern Rules
Rules with parameters using `@{...}` syntax:

##### Unique Numbers
```python
{"type": "int", "rule": "@{4}unique"}     # Unique 4-digit numbers
{"type": "int", "rule": "@{6}unique"}     # Unique 6-digit numbers
```

##### Range Values
```python
{"type": "int", "rule": "@{1-100}range"}        # Integer between 1-100
{"type": "float", "rule": "@{0.0-10.0}range"}   # Float between 0.0-10.0
```

##### Fixed Length
```python
{"type": "str", "rule": "@{8}length"}     # 8-character random string
{"type": "int", "rule": "@{5}length"}     # 5-digit random number
```

##### Choice Selection
```python
{"type": "str", "rule": "@{red,green,blue}choice"}        # Pick from colors
{"type": "str", "rule": "@{admin,user,guest}choice"}      # Pick from roles
```

##### Format Templates
```python
{"type": "str", "rule": "@{ABC-####}format"}     # ABC-1234 (# = digit)
{"type": "str", "rule": "@{???-###}format"}      # XYZ-123 (? = letter)
{"type": "str", "rule": "@{AA##AA}format"}       # AB12CD (A = uppercase)
```

Format placeholders:
- `#` → Random digit (0-9)
- `?` → Random letter (a-z, A-Z)
- `A` → Random uppercase letter
- `a` → Random lowercase letter

#### 3. File-based Rules
Load data from external files:
```python
generator.load_file_data('usernames', 'data/usernames.txt')
{"type": "str", "rule": "usernames"}  # Uses loaded data
```

#### 4. Custom Rules
User-defined generator functions:
```python
def generate_department():
    return random.choice(['Engineering', 'Marketing', 'Sales'])

generator.add_custom_rule('department', generate_department)
{"type": "str", "rule": "department"}  # Uses custom function
```

## Built-in Rules

### Identity & Personal
| Rule | Type | Description | Example |
|------|------|-------------|---------|
| `email` | str | Email addresses | `john.doe@gmail.com` |
| `username` | str | Usernames | `user_123` |
| `password` | str | Passwords | `P@ssw0rd123` |
| `name` | str | Full names | `John Smith` |
| `firstname` | str | First names | `John` |
| `lastname` | str | Last names | `Smith` |
| `phone` | str | Phone numbers | `+1-555-123-4567` |
| `age` | int | Ages (18-85) | `32` |

### Location & Address
| Rule | Type | Description | Example |
|------|------|-------------|---------|
| `address` | str | Street addresses | `123 Main St` |
| `city` | str | City names | `New York` |
| `country` | str | Country names | `USA` |
| `zipcode` | str | ZIP codes | `12345` |

### Business & Commerce
| Rule | Type | Description | Example |
|------|------|-------------|---------|
| `company` | str | Company names | `Tech Solutions` |
| `price` | float | Prices | `99.99` |
| `rating` | float | Ratings (1.0-5.0) | `4.2` |
| `score` | int | Scores (0-100) | `85` |
| `id` | int | ID numbers | `12345` |

### Time & Date
| Rule | Type | Description | Example |
|------|------|-------------|---------|
| `timestamp` | int | Unix timestamps | `1634567890` |
| `date` | str | ISO dates | `2023-10-15` |
| `time` | str | Time strings | `14:30:25` |
| `datetime` | str | ISO datetime | `2023-10-15T14:30:25` |

### Text & Content
| Rule | Type | Description | Example |
|------|------|-------------|---------|
| `title` | str | Titles | `Amazing Product` |
| `description` | str | Descriptions | `High-quality product...` |
| `paragraph` | str | Lorem ipsum text | `Lorem ipsum dolor...` |
| `sentence` | str | Single sentences | `The system provides...` |
| `word` | str | Single words | `example` |

### Web & Tech
| Rule | Type | Description | Example |
|------|------|-------------|---------|
| `url` | str | URLs | `https://example.com` |
| `uuid` | str | UUIDs | `550e8400-e29b...` |

### Boolean & Status
| Rule | Type | Description | Example |
|------|------|-------------|---------|
| `bool` | bool | Random booleans | `true` |
| `active` | bool | Active status | `false` |

## Custom Rules

### Adding Custom Rules

Create custom generator functions and register them:

```python
def generate_skill_level():
    """Generate programming skill levels"""
    levels = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
    return random.choice(levels)

def generate_priority():
    """Generate task priorities with weights"""
    priorities = ['Low', 'Medium', 'High', 'Critical']
    weights = [40, 30, 20, 10]  # Lower priorities more common
    return random.choices(priorities, weights=weights)[0]

def generate_version():
    """Generate semantic version numbers"""
    major = random.randint(1, 5)
    minor = random.randint(0, 20)
    patch = random.randint(0, 50)
    return f"{major}.{minor}.{patch}"

# Register custom rules
generator.add_custom_rule('skill_level', generate_skill_level)
generator.add_custom_rule('priority', generate_priority)
generator.add_custom_rule('version', generate_version)

# Use in schema
schema = {
    "skill": {"type": "str", "rule": "skill_level"},
    "priority": {"type": "str", "rule": "priority"},
    "version": {"type": "str", "rule": "version"}
}
```

### Custom Rules with Parameters

For more complex rules, access the generator instance:

```python
def generate_weighted_age(min_age=18, max_age=65, weights=None):
    """Generate age with custom weights for different ranges"""
    if weights is None:
        weights = [10, 40, 30, 15, 5]  # 18-25, 26-35, 36-45, 46-55, 56-65
    
    age_ranges = [(18, 25), (26, 35), (36, 45), (46, 55), (56, 65)]
    selected_range = random.choices(age_ranges, weights=weights)[0]
    return random.randint(selected_range[0], selected_range[1])

generator.add_custom_rule('weighted_age', generate_weighted_age)
```

## File-based Data

### Loading External Data

Load realistic data from files for more authentic generation:

```python
# Load data from files
generator.load_file_data('real_names', 'data/names.txt')
generator.load_file_data('companies', 'data/companies.txt')
generator.load_file_data('domains', 'data/email_domains.txt')

# Use loaded data in schema
schema = {
    "name": {"type": "str", "rule": "real_names"},
    "company": {"type": "str", "rule": "companies"},
    "domain": {"type": "str", "rule": "domains"}
}
```

### File Format

Data files should contain one item per line:

**names.txt:**
```
John Smith
Jane Doe
Michael Johnson
Sarah Williams
David Brown
```

**companies.txt:**
```
Apple Inc.
Microsoft Corporation
Google LLC
Amazon.com Inc.
Meta Platforms Inc.
```

You can use the [usernames.txt](./usernames.txt) and [passwords.txt](./passwords.txt) files in this repo (from [SecLists](https://gitlab.com/kalilinux/packages/seclists)) to get real usernames and passwords rather than the built-in rules to generate them

### Combining File Data with Rules

Create hybrid rules that combine file data with patterns:

```python
def generate_work_email():
    """Generate work email using real names and company domains"""
    names = generator.file_data.get('real_names', ['john.doe'])
    domains = generator.file_data.get('company_domains', ['company.com'])
    
    name = random.choice(names).lower().replace(' ', '.')
    domain = random.choice(domains)
    
    return f"{name}@{domain}"

generator.add_custom_rule('work_email', generate_work_email)
```

## API Reference

### Class: JSONGenerator

#### Constructor
```python
generator = JSONGenerator()
```

#### Methods

##### set_schema(schema: Dict[str, Any])
Set the JSON schema for generation.

**Parameters:**
- `schema`: Dictionary defining the structure and rules

**Example:**
```python
schema = {
    "id": {"type": "int", "rule": "@{6}unique"},
    "name": {"type": "str", "rule": "name"}
}
generator.set_schema(schema)
```

##### add_custom_rule(name: str, generator_func: Callable)
Add a custom rule generator function.

**Parameters:**
- `name`: Rule name to use in schema
- `generator_func`: Function that returns generated values

**Example:**
```python
def custom_status():
    return random.choice(['active', 'inactive', 'pending'])

generator.add_custom_rule('status', custom_status)
```

##### load_file_data(data_type: str, file_path: str)
Load data from file for use in generation.

**Parameters:**
- `data_type`: Name to reference the data
- `file_path`: Path to file with one item per line

**Example:**
```python
generator.load_file_data('usernames', 'data/usernames.txt')
```

##### generate(count: int = 1, as_string: bool = False) → Union[List[str], List[Dict]]
Generate multiple JSON objects or strings.

**Parameters:**
- `count`: Number of objects to generate (default: 1)
- `as_string`: Return JSON strings if True, objects if False (default: False)

**Returns:**
- List of JSON strings or dictionary objects

**Example:**
```python
# Generate 5 objects
objects = generator.generate(5)

# Generate 3 JSON strings
json_strings = generator.generate(3, as_string=True)
```

##### generate_single(as_string: bool = False) → Union[str, Dict]
Generate a single JSON object or string.

**Parameters:**
- `as_string`: Return JSON string if True, object if False (default: False)

**Returns:**
- JSON string or dictionary object

**Example:**
```python
# Generate single object
user = generator.generate_single()

# Generate single JSON string
user_json = generator.generate_single(as_string=True)
```

## Advanced Examples

### E-commerce Product Catalog

```python
# Complex e-commerce schema
ecommerce_schema = {
    "product_id": {"type": "str", "rule": "@{PROD-######}format"},
    "name": {"type": "str", "rule": "title"},
    "description": {"type": "str", "rule": "description"},
    "price": {"type": "float", "rule": "@{9.99-999.99}range"},
    "category": {"type": "str", "rule": "@{Electronics,Clothing,Books,Home,Sports}choice"},
    "in_stock": {"type": "bool", "rule": "bool"},
    "rating": {"type": "float", "rule": "rating"},
    "reviews_count": {"type": "int", "rule": "@{0-500}range"},
    "tags": {
        "type": "array",
        "items": {"type": "str", "rule": "@{popular,bestseller,new,sale,premium}choice"},
        "length": 2
    },
    "specifications": {
        "type": "object",
        "properties": {
            "weight": {"type": "float", "rule": "@{0.1-50.0}range"},
            "dimensions": {"type": "str", "rule": "@{##.#x##.#x##.#}format"},
            "warranty_months": {"type": "int", "rule": "@{6,12,24,36}choice"}
        }
    },
    "vendor": {
        "type": "object",
        "properties": {
            "name": {"type": "str", "rule": "company"},
            "contact_email": {"type": "str", "rule": "email"},
            "rating": {"type": "float", "rule": "@{3.0-5.0}range"}
        }
    }
}

generator.set_schema(ecommerce_schema)
products = generator.generate(10)
```

### User Management System

```python
# User management with roles and permissions
user_schema = {
    "user_id": {"type": "int", "rule": "@{8}unique"},
    "username": {"type": "str", "rule": "username"},
    "email": {"type": "str", "rule": "email"},
    "full_name": {"type": "str", "rule": "name"},
    "role": {"type": "str", "rule": "@{admin,moderator,editor,user}choice"},
    "status": {"type": "str", "rule": "@{active,inactive,suspended,pending}choice"},
    "created_at": {"type": "str", "rule": "datetime"},
    "last_login": {"type": "str", "rule": "datetime"},
    "profile": {
        "type": "object",
        "properties": {
            "avatar": {"type": "str", "rule": "url"},
            "bio": {"type": "str", "rule": "paragraph"},
            "location": {"type": "str", "rule": "city"},
            "website": {"type": "str", "rule": "url"},
            "social_links": {
                "type": "array",
                "items": {"type": "str", "rule": "url"},
                "length": 3
            }
        }
    },
    "permissions": {
        "type": "array",
        "items": {"type": "str", "rule": "@{read,write,delete,admin,moderate}choice"},
        "length": 4
    },
    "preferences": {
        "type": "object",
        "properties": {
            "theme": {"type": "str", "rule": "@{light,dark,auto}choice"},
            "notifications": {"type": "bool", "rule": "bool"},
            "language": {"type": "str", "rule": "@{en,es,fr,de,ja}choice"}
        }
    }
}

# Add custom rules for this domain
def generate_department():
    return random.choice(['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations'])

def generate_seniority():
    return random.choice(['Junior', 'Mid', 'Senior', 'Lead', 'Principal', 'Director'])

generator.add_custom_rule('department', generate_department)
generator.add_custom_rule('seniority', generate_seniority)

# Extend schema with custom fields
user_schema.update({
    "department": {"type": "str", "rule": "department"},
    "seniority": {"type": "str", "rule": "seniority"}
})

generator.set_schema(user_schema)
users = generator.generate(20)
```

### IoT Device Data

```python
# IoT sensor data simulation
iot_schema = {
    "device_id": {"type": "str", "rule": "@{IOT-########}format"},
    "device_type": {"type": "str", "rule": "@{temperature,humidity,pressure,light,motion}choice"},
    "location": {"type": "str", "rule": "@{room_###}format"},
    "timestamp": {"type": "int", "rule": "timestamp"},
    "status": {"type": "str", "rule": "@{online,offline,maintenance,error}choice"},
    "battery_level": {"type": "int", "rule": "@{0-100}range"},
    "firmware_version": {"type": "str", "rule": "@{#.#.##}format"},
    "readings": {
        "type": "object",
        "properties": {
            "value": {"type": "float", "rule": "@{-10.0-50.0}range"},
            "unit": {"type": "str", "rule": "@{celsius,fahrenheit,percent,lux,pa}choice"},
            "accuracy": {"type": "float", "rule": "@{95.0-99.9}range"}
        }
    },
    "network_info": {
        "type": "object",
        "properties": {
            "ip_address": {"type": "str", "rule": "@{192.168.1.###}format"},
            "signal_strength": {"type": "int", "rule": "@{-100--30}range"},
            "protocol": {"type": "str", "rule": "@{WiFi,Bluetooth,Zigbee,LoRa}choice"}
        }
    },
    "alerts": {
        "type": "array",
        "items": {"type": "str", "rule": "@{low_battery,high_temp,connection_lost,calibration_needed}choice"},
        "length": 1
    }
}

generator.set_schema(iot_schema)
iot_data = generator.generate(50)
```

## Best Practices

### Schema Design

1. **Use Descriptive Field Names**
   ```python
   # Good
   {"user_id": {"type": "int", "rule": "@{8}unique"}}
   
   # Less clear
   {"id": {"type": "int", "rule": "@{8}unique"}}
   ```

2. **Choose Appropriate Types**
   ```python
   # Use specific types for better data integrity
   {"price": {"type": "float", "rule": "@{9.99-999.99}range"}}  # Not str
   {"is_active": {"type": "bool", "rule": "bool"}}              # Not str
   ```

3. **Leverage Nested Objects**
   ```python
   # Group related fields
   {
       "address": {
           "type": "object",
           "properties": {
               "street": {"type": "str", "rule": "address"},
               "city": {"type": "str", "rule": "city"},
               "zipcode": {"type": "str", "rule": "zipcode"}
           }
       }
   }
   ```

### Performance Optimization

1. **Limit Unique Value Tracking**
   - Use unique rules sparingly for large datasets
   - Consider using UUIDs for truly unique values

2. **Batch Generation**
   ```python
   # Generate in batches for large datasets
   all_records = []
   batch_size = 1000
   
   for i in range(0, total_records, batch_size):
       batch = generator.generate(min(batch_size, total_records - i))
       all_records.extend(batch)
   ```

3. **File Data Management**
   - Load file data once and reuse
   - Use smaller files for better memory usage

### Data Quality

1. **Use Realistic Constraints**
   ```python
   # Realistic age ranges
   {"age": {"type": "int", "rule": "@{18-65}range"}}
   
   # Realistic ratings
   {"rating": {"type": "float", "rule": "@{1.0-5.0}range"}}
   ```

2. **Combine Multiple Rules**
   ```python
   def generate_realistic_email():
       domains = ['gmail.com', 'yahoo.com', 'company.com']
       first = random.choice(['john', 'jane', 'mike', 'sarah'])
       last = random.choice(['smith', 'doe', 'johnson'])
       return f"{first}.{last}@{random.choice(domains)}"
   ```

3. **Validate Generated Data**
   ```python
   # Add validation after generation
   def validate_user(user):
       assert '@' in user['email']
       assert 18 <= user['age'] <= 65
       assert user['rating'] <= 5.0
       return True
   
   users = generator.generate(100)
   valid_users = [u for u in users if validate_user(u)]
   ```

## Troubleshooting

### Common Issues

#### 1. Unique Value Exhaustion
**Problem:** Getting duplicate values when using `@{N}unique`

**Solution:**
```python
# Increase digit count or use UUIDs
{"id": {"type": "str", "rule": "uuid"}}  # Instead of unique numbers

# Or use larger unique ranges
{"id": {"type": "int", "rule": "@{10}unique"}}  # 10-digit numbers
```

#### 2. File Loading Errors
**Problem:** `FileNotFoundError` when loading data files

**Solution:**
```python
# Check file exists before loading
import os
if os.path.exists('data/usernames.txt'):
    generator.load_file_data('usernames', 'data/usernames.txt')
else:
    print("Warning: usernames.txt not found, using default generation")
```

#### 3. Type Conversion Issues
**Problem:** Values not matching expected types

**Solution:**
```python
# Ensure rule matches type
{"price": {"type": "float", "rule": "@{9.99-199.99}range"}}  # Range for float
{"count": {"type": "int", "rule": "@{1-100}range"}}         # Range for int
```

#### 4. Memory Issues with Large Datasets
**Problem:** Memory usage too high for large generations

**Solution:**
```python
# Use generators for streaming
def generate_stream(count, batch_size=1000):
    for i in range(0, count, batch_size):
        batch = generator.generate(min(batch_size, count - i))
        yield from batch

# Process in batches
for record in generate_stream(100000):
    process_record(record)  # Process one at a time
```

#### 5. Rule Not Found Errors
**Problem:** Custom rules not being recognized

**Solution:**
```python
# Verify rule registration
print(generator.custom_rules.keys())  # Check registered rules

# Ensure function is callable
def my_rule():
    return "test"

generator.add_custom_rule('my_rule', my_rule)  # Not my_rule()
```

### Debugging Tips

1. **Test Schema Components**
   ```python
   # Test individual fields
   test_schema = {"test_field": {"type": "str", "rule": "problematic_rule"}}
   generator.set_schema(test_schema)
   result = generator.generate_single()
   print(result)
   ```

2. **Validate Rule Output**
   ```python
   # Test custom rules directly
   def debug_rule():
       result = my_custom_rule()
       print(f"Rule output: {result}, type: {type(result)}")
       return result
   ```

3. **Check Generated Values**
   ```python
   # Inspect generated data
   sample = generator.generate(5)
   for i, item in enumerate(sample):
       print(f"Item {i}: {json.dumps(item, indent=2)}")
   ```

### Performance Monitoring

```python
import time

# Monitor generation time
start_time = time.time()
data = generator.generate(1000)
generation_time = time.time() - start_time

print(f"Generated 1000 records in {generation_time:.2f} seconds")
print(f"Rate: {1000/generation_time:.2f} records/second")
```

---

## License

This documentation and code are provided as-is for educational and commercial use. Feel free to modify and extend the JSONGenerator class for your specific needs.
