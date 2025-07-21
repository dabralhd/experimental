# Metaclass vs Base Class in Python

## Key Differences

| Aspect | Base Class | Metaclass |
|--------|------------|-----------|
| **Purpose** | Provides behavior to instances | Controls how classes are created |
| **Level** | Instance level (objects) | Class level (classes themselves) |
| **Inheritance** | `class Child(Parent):` | `class MyClass(metaclass=MyMeta):` |
| **When called** | When creating objects | When creating classes |
| **Common use** | Code reuse, polymorphism | Class factories, validation, singletons |

## Base Class Example

```python
class Animal:  # Base class
    def speak(self):
        return "Some sound"

class Dog(Animal):  # Inherits from base class
    def speak(self):
        return "Woof!"

# Usage: Create instances
my_dog = Dog()  # Animal behavior available to Dog instances
```

## Metaclass Example

```python
class LoggingMeta(type):  # Metaclass
    def __new__(mcs, name, bases, namespace):
        print(f"Creating class: {name}")
        return super().__new__(mcs, name, bases, namespace)

class Database(metaclass=LoggingMeta):  # Created by metaclass
    pass

# Usage: Metaclass controls class creation
# When Database class is defined, LoggingMeta.__new__ is called
```

## When to Use Each

### Use Base Classes When:
- You want to share common behavior between classes
- You need polymorphism (different classes with same interface)
- You want to reuse code across multiple classes
- You're working with instances/objects

### Use Metaclasses When:
- You need to control how classes are created
- You want to add class-level attributes/methods automatically
- You need to validate class definitions
- You're implementing design patterns like Singleton
- You're working with the class itself, not instances

## Practical Examples

### Base Class: Animal Hierarchy
```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return f"{self.name} barks"

class Cat(Animal):
    def speak(self):
        return f"{self.name} meows"
```

### Metaclass: Singleton Pattern
```python
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=SingletonMeta):
    pass

# Only one Config instance can exist
```

## Key Takeaway

- **Base Class**: "I want my objects to have this behavior"
- **Metaclass**: "I want my classes to be created this way"

Think of base classes as templates for objects, and metaclasses as templates for classes! 