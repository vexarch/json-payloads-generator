import json
import random
import string
import uuid
import datetime
from typing import Any, Dict, List, Union, Callable, Optional
from pathlib import Path
import re

class JSONGenerator:
    """
    A flexible JSON generator with rule-based placeholders for generating realistic test data.
    """
    
    def __init__(self):
        self.schema = {}
        self.custom_rules = {}
        self.file_data = {}
        self.generated_values = {}
        
        self.builtin_patterns = {
            'unique': r'@{(\d+)}unique',
            'range': r'@{(\d+)-(\d+)}range',
            'length': r'@{(\d+)}length',
            'choice': r'@{([^}]+)}choice',
            'format': r'@{([^}]+)}format'
        }
        
        self._init_builtin_rules()
    
    def _init_builtin_rules(self):
        """Initialize built-in value generation rules."""
        self.builtin_rules = {
            # Basic generators
            'email': self._generate_email,
            'username': self._generate_username,
            'password': self._generate_password,
            'phone': self._generate_phone,
            'url': self._generate_url,
            'uuid': self._generate_uuid,
            'name': self._generate_name,
            'firstname': self._generate_firstname,
            'lastname': self._generate_lastname,
            'company': self._generate_company,
            'address': self._generate_address,
            'city': self._generate_city,
            'country': self._generate_country,
            'zipcode': self._generate_zipcode,
            
            # Time generators
            'timestamp': self._generate_timestamp,
            'date': self._generate_date,
            'time': self._generate_time,
            'datetime': self._generate_datetime,
            'age': self._generate_age,
            
            # Numeric generators
            'id': self._generate_id,
            'price': self._generate_price,
            'rating': self._generate_rating,
            'score': self._generate_score,
            
            # Text generators
            'title': self._generate_title,
            'description': self._generate_description,
            'paragraph': self._generate_paragraph,
            'sentence': self._generate_sentence,
            'word': self._generate_word,
            
            # Boolean generators
            'bool': self._generate_bool,
            'active': self._generate_active,
        }
    
    def set_schema(self, schema: Dict[str, Any]):
        """
        Set the JSON schema with keys, types, and rules.
        
        Example schema:
        {
            "id": {"type": "int", "rule": "@{4}unique"},
            "name": {"type": "str", "rule": "firstname"},
            "email": {"type": "str", "rule": "email"},
            "age": {"type": "int", "rule": "@{18-80}range"},
            "active": {"type": "bool", "rule": "bool"},
            "tags": {"type": "array", "items": {"type": "str", "rule": "@{programming,design,marketing}choice"}, "length": 3},
            "profile": {
                "type": "object",
                "properties": {
                    "bio": {"type": "str", "rule": "description"},
                    "score": {"type": "float", "rule": "@{0.0-10.0}range"}
                }
            }
        }
        """
        self.schema = schema
        self.generated_values = {}  # Reset unique tracking
    
    def add_custom_rule(self, name: str, generator: Callable):
        """Add a custom rule generator function."""
        self.custom_rules[name] = generator
    
    def load_file_data(self, data_type: str, file_path: str):
        """
        Load data from file for use in generation.
        
        Args:
            data_type: Name of the data type (e.g., 'usernames', 'emails')
            file_path: Path to file containing one item per line
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.file_data[data_type] = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Warning: File {file_path} not found for {data_type}")
            self.file_data[data_type] = []
    
    def _parse_rule(self, rule: str) -> tuple:
        """Parse rule string to extract parameters."""
        if not rule.startswith('@{'):
            return rule, {}
        
        for pattern_name, pattern in self.builtin_patterns.items():
            match = re.match(pattern, rule)
            if match:
                return pattern_name, match.groups()
        
        return rule, {}
    
    def _generate_value(self, field_config: Dict[str, Any], field_name: str = "") -> Any:
        """Generate value based on field configuration."""
        field_type = field_config.get('type', 'str')
        rule = field_config.get('rule', '')
        
        if field_type == 'array':
            length = field_config.get('length', random.randint(1, 5))
            items_config = field_config.get('items', {'type': 'str', 'rule': 'word'})
            return [self._generate_value(items_config, f"{field_name}_{i}") for i in range(length)]
        
        if field_type == 'object':
            properties = field_config.get('properties', {})
            return {key: self._generate_value(prop_config, f"{field_name}.{key}") 
                   for key, prop_config in properties.items()}
        
        rule_type, params = self._parse_rule(rule)
        
        if rule_type in self.custom_rules:
            value = self.custom_rules[rule_type]()
        elif rule_type in self.builtin_rules:
            value = self.builtin_rules[rule_type]()
        elif rule_type == 'unique':
            digits = int(params[0])
            value = self._generate_unique_number(digits, field_name)
        elif rule_type == 'range':
            min_val, max_val = params
            if field_type in ['int']:
                value = random.randint(int(min_val), int(max_val))
            elif field_type in ['float', 'double']:
                value = random.uniform(float(min_val), float(max_val))
            else:
                value = random.randint(int(min_val), int(max_val))
        elif rule_type == 'length':
            length = int(params[0])
            if field_type == 'str':
                value = ''.join(random.choices(string.ascii_letters, k=length))
            else:
                value = random.randint(10**(length-1), 10**length - 1)
        elif rule_type == 'choice':
            choices = params[0].split(',')
            value = random.choice(choices).strip()
        elif rule_type == 'format':
            format_str = params[0]
            value = self._apply_format(format_str)
        elif rule in self.file_data and self.file_data[rule]:
            value = random.choice(self.file_data[rule])
        else:
            value = self._generate_default_value(field_type)
        
        return self._convert_type(value, field_type)
    
    def _generate_unique_number(self, digits: int, field_name: str) -> int:
        """Generate unique number with specified digits."""
        if field_name not in self.generated_values:
            self.generated_values[field_name] = set()
        
        min_val = 10**(digits-1) if digits > 1 else 0
        max_val = 10**digits - 1
        
        for _ in range(1000):
            value = random.randint(min_val, max_val)
            if value not in self.generated_values[field_name]:
                self.generated_values[field_name].add(value)
                return value
        
        # Fallback: use timestamp suffix
        return int(str(random.randint(min_val, max_val//10)) + str(int(datetime.datetime.now().timestamp()))[-2:])
    
    def _apply_format(self, format_str: str) -> str:
        """Apply format string with placeholders."""
        result = format_str
        result = result.replace('#', str(random.randint(0, 9)))
        result = result.replace('A', random.choice(string.ascii_uppercase))
        result = result.replace('a', random.choice(string.ascii_lowercase))
        result = result.replace('?', random.choice(string.ascii_letters))
        return result
    
    def _convert_type(self, value: Any, target_type: str) -> Any:
        """Convert value to target type."""
        if target_type == 'int':
            return int(float(str(value)))
        elif target_type in ['float', 'double']:
            return float(value)
        elif target_type == 'bool':
            return bool(value) if isinstance(value, (int, float)) else value
        elif target_type == 'str':
            return str(value)
        return value
    
    def _generate_default_value(self, field_type: str) -> Any:
        """Generate default value based on type."""
        if field_type == 'int':
            return random.randint(1, 1000)
        elif field_type in ['float', 'double']:
            return round(random.uniform(0, 100), 2)
        elif field_type == 'bool':
            return random.choice([True, False])
        elif field_type == 'str':
            return ''.join(random.choices(string.ascii_letters, k=8))
        return None
    
    def _generate_email(self):
        domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'company.com']
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(5, 12)))
        return f"{username}@{random.choice(domains)}"
    
    def _generate_username(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits + '_', k=random.randint(5, 15)))
    
    def _generate_password(self):
        chars = string.ascii_letters + string.digits + '!@#$%^&*'
        return ''.join(random.choices(chars, k=random.randint(8, 16)))
    
    def _generate_phone(self):
        return f"+1-{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}"
    
    def _generate_url(self):
        domains = ['example.com', 'test.org', 'demo.net', 'sample.io']
        paths = ['', '/api', '/users', '/products', '/about', '/contact']
        return f"https://www.{random.choice(domains)}{random.choice(paths)}"
    
    def _generate_uuid(self):
        return str(uuid.uuid4())
    
    def _generate_name(self):
        first_names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Chris', 'Anna', 'Tom', 'Mary']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Wilson', 'Moore']
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _generate_firstname(self):
        names = ['John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Chris', 'Anna', 'Tom', 'Mary', 'Alex', 'Emma']
        return random.choice(names)
    
    def _generate_lastname(self):
        names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Wilson', 'Moore']
        return random.choice(names)
    
    def _generate_company(self):
        prefixes = ['Tech', 'Global', 'Smart', 'Digital', 'Advanced', 'Modern', 'Future']
        suffixes = ['Solutions', 'Systems', 'Corp', 'Industries', 'Technologies', 'Innovations', 'Services']
        return f"{random.choice(prefixes)} {random.choice(suffixes)}"
    
    def _generate_address(self):
        streets = ['Main St', 'Oak Ave', 'Park Rd', 'First St', 'Second Ave', 'Elm St', 'Maple Dr']
        return f"{random.randint(1, 9999)} {random.choice(streets)}"
    
    def _generate_city(self):
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio']
        return random.choice(cities)
    
    def _generate_country(self):
        countries = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Japan', 'Australia', 'Brazil']
        return random.choice(countries)
    
    def _generate_zipcode(self):
        return f"{random.randint(10000, 99999)}"
    
    def _generate_timestamp(self):
        return int(datetime.datetime.now().timestamp())
    
    def _generate_date(self):
        start = datetime.date(2020, 1, 1)
        end = datetime.date.today()
        delta = end - start
        random_days = random.randint(0, delta.days)
        return (start + datetime.timedelta(days=random_days)).isoformat()
    
    def _generate_time(self):
        return f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
    
    def _generate_datetime(self):
        return datetime.datetime.now().isoformat()
    
    def _generate_age(self):
        return random.randint(18, 85)
    
    def _generate_id(self):
        return random.randint(1, 999999)
    
    def _generate_price(self):
        return round(random.uniform(9.99, 999.99), 2)
    
    def _generate_rating(self):
        return round(random.uniform(1.0, 5.0), 1)
    
    def _generate_score(self):
        return random.randint(0, 100)
    
    def _generate_title(self):
        adjectives = ['Amazing', 'Incredible', 'Awesome', 'Great', 'Fantastic', 'Perfect', 'Ultimate']
        nouns = ['Product', 'Service', 'Solution', 'Tool', 'System', 'Platform', 'Application']
        return f"{random.choice(adjectives)} {random.choice(nouns)}"
    
    def _generate_description(self):
        descriptions = [
            "This is a high-quality product designed for modern users.",
            "An innovative solution that meets all your needs.",
            "Professional service with excellent customer support.",
            "State-of-the-art technology for better performance.",
            "Reliable and efficient system for everyday use."
        ]
        return random.choice(descriptions)
    
    def _generate_paragraph(self):
        sentences = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco.",
            "Duis aute irure dolor in reprehenderit in voluptate velit esse."
        ]
        return " ".join(random.choices(sentences, k=random.randint(2, 4)))
    
    def _generate_sentence(self):
        subjects = ['The system', 'This product', 'Our solution', 'The application']
        verbs = ['provides', 'offers', 'delivers', 'ensures', 'guarantees']
        objects = ['excellent performance', 'great results', 'outstanding quality', 'reliable service']
        return f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(objects)}."
    
    def _generate_word(self):
        words = ['example', 'sample', 'test', 'demo', 'data', 'value', 'item', 'element']
        return random.choice(words)
    
    def _generate_bool(self):
        return random.choice([True, False])
    
    def _generate_active(self):
        return random.choice([True, False])
    
    def generate(self, count: int = 1, as_string: bool = False) -> Union[List[str], List[Dict]]:
        """
        Generate n unique JSON objects/strings.
        
        Args:
            count: Number of objects to generate
            as_string: Return as JSON strings if True, objects if False
            
        Returns:
            List of JSON strings or dictionary objects
        """
        results = []
        
        for i in range(count):
            # Generate object based on schema
            obj = {}
            for key, config in self.schema.items():
                obj[key] = self._generate_value(config, f"{key}_{i}")
            
            if as_string:
                results.append(json.dumps(obj, indent=2))
            else:
                results.append(obj)
        
        return results
    
    def generate_single(self, as_string: bool = False) -> Union[str, Dict]:
        """Generate a single JSON object/string."""
        return self.generate(1, as_string)[0]


if __name__ == "__main__":
    generator = JSONGenerator()
    
    schema = {
        "id": {"type": "int", "rule": "@{6}unique"},
        "username": {"type": "str", "rule": "username"},
        "email": {"type": "str", "rule": "email"},
        "name": {"type": "str", "rule": "name"},
        "age": {"type": "int", "rule": "@{18-65}range"},
        "salary": {"type": "float", "rule": "@{30000-150000}range"},
        "active": {"type": "bool", "rule": "bool"},
        "phone": {"type": "str", "rule": "phone"},
        "website": {"type": "str", "rule": "url"},
        "tags": {
            "type": "array",
            "items": {"type": "str", "rule": "@{python,javascript,java,go,rust}choice"},
            "length": 3
        },
        "profile": {
            "type": "object",
            "properties": {
                "bio": {"type": "str", "rule": "description"},
                "rating": {"type": "float", "rule": "rating"},
                "joined_date": {"type": "str", "rule": "date"}
            }
        },
        "code": {"type": "str", "rule": "@{ABC-####}format"}
    }
    
    generator.set_schema(schema)
    
    def custom_department():
        return random.choice(['Engineering', 'Marketing', 'Sales', 'HR', 'Finance'])
    
    generator.add_custom_rule('department', custom_department)
    
    print("=== Generated JSON Objects ===")
    objects = generator.generate(3, as_string=False)
    for i, obj in enumerate(objects, 1):
        print(f"\nObject {i}:")
        print(json.dumps(obj, indent=2))
    
    print("\n=== Generated JSON Strings ===")
    strings = generator.generate(2, as_string=True)
    for i, json_str in enumerate(strings, 1):
        print(f"\nJSON String {i}:")
        print(json_str)
