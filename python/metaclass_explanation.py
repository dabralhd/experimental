"""
Understanding Metaclasses vs Base Classes in Python

Key Differences:
- Base Class: Inherits behavior to instances (objects)
- Metaclass: Controls how classes are created and behave
"""

# ============================================================================
# BASE CLASS EXAMPLE (Regular Inheritance)
# ============================================================================

class Animal:  # This is a base class
    """Base class that provides common behavior for animals."""
    
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return f"{self.name} makes a sound"
    
    def move(self):
        return f"{self.name} moves"


class Dog(Animal):  # Dog inherits from Animal (base class)
    """Dog class inherits behavior from Animal base class."""
    
    def speak(self):
        return f"{self.name} barks: Woof!"
    
    def fetch(self):
        return f"{self.name} fetches the ball"


class Cat(Animal):  # Cat also inherits from Animal (base class)
    """Cat class inherits behavior from Animal base class."""
    
    def speak(self):
        return f"{self.name} meows: Meow!"
    
    def climb(self):
        return f"{self.name} climbs the tree"


# ============================================================================
# METACLASS EXAMPLE (Class Factory)
# ============================================================================

class LoggingMeta(type):
    """
    Metaclass that adds logging functionality to all classes it creates.
    This operates at the CLASS level, not instance level.
    """
    
    def __new__(mcs, name, bases, namespace):
        """Called when creating a new class."""
        print(f"Creating class: {name}")
        
        # Add a class-level attribute
        namespace['_created_by_metaclass'] = True
        
        # Add a method to the class
        def log_creation(cls):
            return f"Class {cls.__name__} was created by LoggingMeta"
        
        namespace['log_creation'] = classmethod(log_creation)
        
        return super().__new__(mcs, name, bases, namespace)
    
    def __call__(cls, *args, **kwargs):
        """Called when creating an instance of the class."""
        print(f"Creating instance of: {cls.__name__}")
        return super().__call__(*args, **kwargs)


# Classes created by the metaclass
class Database(metaclass=LoggingMeta):
    """This class is created by LoggingMeta metaclass."""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
    
    def connect(self):
        return f"Connected to {self.connection_string}"


class Cache(metaclass=LoggingMeta):
    """This class is also created by LoggingMeta metaclass."""
    
    def __init__(self):
        self.data = {}
    
    def set(self, key, value):
        self.data[key] = value


# ============================================================================
# COMPARISON: Base Class vs Metaclass
# ============================================================================

def demonstrate_differences():
    """Show the key differences between base classes and metaclasses."""
    
    print("=" * 60)
    print("BASE CLASS vs METACLASS COMPARISON")
    print("=" * 60)
    
    # Base Class Example
    print("\n1. BASE CLASS (Regular Inheritance):")
    print("-" * 40)
    
    # Create instances
    my_dog = Dog("Buddy")
    my_cat = Cat("Whiskers")
    
    print(f"Dog instance: {my_dog}")
    print(f"Cat instance: {my_cat}")
    print(f"Dog speaks: {my_dog.speak()}")
    print(f"Cat speaks: {my_cat.speak()}")
    print(f"Dog can fetch: {my_dog.fetch()}")
    print(f"Cat can climb: {my_cat.climb()}")
    
    # Check inheritance
    print(f"\nInheritance check:")
    print(f"Is Dog a subclass of Animal? {issubclass(Dog, Animal)}")
    print(f"Is my_dog an instance of Animal? {isinstance(my_dog, Animal)}")
    
    # Metaclass Example
    print("\n2. METACLASS (Class Factory):")
    print("-" * 40)
    
    # Create instances (notice the metaclass __call__ is triggered)
    db = Database("postgresql://localhost:5432/mydb")
    cache = Cache()
    
    print(f"Database instance: {db}")
    print(f"Cache instance: {cache}")
    
    # Check metaclass attributes
    print(f"\nMetaclass attributes:")
    print(f"Database._created_by_metaclass: {Database._created_by_metaclass}")
    print(f"Cache._created_by_metaclass: {Cache._created_by_metaclass}")
    print(f"Database.log_creation(): {Database.log_creation()}")
    print(f"Cache.log_creation(): {Cache.log_creation()}")
    
    # Check metaclass relationships
    print(f"\nMetaclass relationships:")
    print(f"Database's metaclass: {type(Database)}")
    print(f"Cache's metaclass: {type(Cache)}")
    print(f"Is Database created by LoggingMeta? {isinstance(Database, LoggingMeta)}")
    print(f"Is Cache created by LoggingMeta? {isinstance(Cache, LoggingMeta)}")


# ============================================================================
# PRACTICAL METACLASS EXAMPLE: Singleton Pattern
# ============================================================================

class SingletonMeta(type):
    """
    Metaclass that ensures only one instance of a class exists.
    This is a practical use case for metaclasses.
    """
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AppConfig(metaclass=SingletonMeta):
    """Application configuration - only one instance can exist."""
    
    def __init__(self):
        self.settings = {
            "debug": False,
            "port": 8000,
            "database_url": "sqlite:///app.db"
        }
        print("AppConfig initialized")
    
    def get_setting(self, key):
        return self.settings.get(key)
    
    def set_setting(self, key, value):
        self.settings[key] = value


def demonstrate_singleton_metaclass():
    """Show how metaclass creates singleton behavior."""
    
    print("\n3. PRACTICAL METACLASS: Singleton Pattern")
    print("-" * 50)
    
    # Create multiple instances
    config1 = AppConfig()
    config2 = AppConfig()
    config3 = AppConfig()
    
    print(f"config1 is config2: {config1 is config2}")
    print(f"config2 is config3: {config2 is config3}")
    
    # Modify one instance, affects all
    config1.set_setting("debug", True)
    print(f"config2 debug setting: {config2.get_setting('debug')}")
    print(f"config3 debug setting: {config3.get_setting('debug')}")


# ============================================================================
# METACLASS FOR VALIDATION
# ============================================================================

class ValidationMeta(type):
    """
    Metaclass that validates class attributes during creation.
    """
    
    def __new__(mcs, name, bases, namespace):
        # Check if required attributes exist
        required_attrs = namespace.get('__required_attrs__', [])
        
        for attr in required_attrs:
            if attr not in namespace:
                raise AttributeError(f"Class {name} must define '{attr}'")
        
        return super().__new__(mcs, name, bases, namespace)


class UserModel(metaclass=ValidationMeta):
    """User model that requires certain attributes."""
    
    __required_attrs__ = ['id', 'name', 'email']
    
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email


def demonstrate_validation_metaclass():
    """Show how metaclass can enforce validation."""
    
    print("\n4. METACLASS FOR VALIDATION")
    print("-" * 40)
    
    try:
        # This should work
        user = UserModel(1, "John Doe", "john@example.com")
        print(f"User created: {user.name}")
        
        # This would fail (uncomment to see error)
        # class InvalidUser(metaclass=ValidationMeta):
        #     __required_attrs__ = ['id', 'name', 'email']
        #     # Missing required attributes
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    demonstrate_differences()
    demonstrate_singleton_metaclass()
    demonstrate_validation_metaclass() 