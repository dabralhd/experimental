"""
Singleton Pattern Implementation in Python

The singleton pattern ensures that a class has only one instance and provides
a global point of access to that instance.
"""

# Method 1: Using __new__ method (Classic approach)
class DatabaseConnection:
    """
    A singleton class representing a database connection.
    Only one instance can exist throughout the application.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection_string = "postgresql://localhost:5432/mydb"
            cls._instance.is_connected = False
            print("Creating new database connection instance")
        return cls._instance
    
    def connect(self):
        if not self.is_connected:
            self.is_connected = True
            print(f"Connected to database: {self.connection_string}")
        else:
            print("Already connected to database")
    
    def disconnect(self):
        if self.is_connected:
            self.is_connected = False
            print("Disconnected from database")
        else:
            print("Not connected to database")
    
    def execute_query(self, query):
        if self.is_connected:
            print(f"Executing query: {query}")
            return f"Result for: {query}"
        else:
            print("Cannot execute query - not connected")
            return None


# Method 2: Using decorator pattern
def singleton(cls):
    """
    Decorator that makes a class a singleton.
    """
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class Logger:
    """
    A singleton logger class using decorator pattern.
    """
    def __init__(self):
        self.log_level = "INFO"
        self.logs = []
        print("Initializing logger")
    
    def log(self, message, level="INFO"):
        log_entry = f"[{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def get_logs(self):
        return self.logs.copy()


# Method 3: Using metaclass
class SingletonMeta(type):
    """
    Metaclass that ensures only one instance of a class exists.
    """
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigurationManager(metaclass=SingletonMeta):
    """
    A singleton configuration manager using metaclass.
    """
    def __init__(self):
        self.config = {
            "app_name": "MyApp",
            "version": "1.0.0",
            "debug": False
        }
        print("Initializing configuration manager")
    
    def get_config(self, key):
        return self.config.get(key)
    
    def set_config(self, key, value):
        self.config[key] = value
        print(f"Updated config: {key} = {value}")
    
    def get_all_config(self):
        return self.config.copy()


# Method 4: Using module-level singleton (Pythonic approach)
class CacheManager:
    """
    A simple cache manager that demonstrates module-level singleton.
    """
    def __init__(self):
        self.cache = {}
        print("Initializing cache manager")
    
    def set(self, key, value):
        self.cache[key] = value
        print(f"Cached: {key} = {value}")
    
    def get(self, key):
        return self.cache.get(key)
    
    def clear(self):
        self.cache.clear()
        print("Cache cleared")


# Create a single instance at module level
cache_manager = CacheManager()


def demonstrate_singleton():
    """
    Demonstrate the singleton pattern with all implementations.
    """
    print("=" * 60)
    print("SINGLETON PATTERN DEMONSTRATION")
    print("=" * 60)
    
    # Test DatabaseConnection singleton
    print("\n1. Database Connection Singleton (__new__ method):")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"db1 is db2: {db1 is db2}")  # Should be True
    
    db1.connect()
    db2.execute_query("SELECT * FROM users")
    
    # Test Logger singleton
    print("\n2. Logger Singleton (Decorator pattern):")
    logger1 = Logger()
    logger2 = Logger()
    print(f"logger1 is logger2: {logger1 is logger2}")  # Should be True
    
    logger1.log("Application started")
    logger2.log("User logged in", "DEBUG")
    print(f"Total logs: {len(logger1.get_logs())}")
    
    # Test ConfigurationManager singleton
    print("\n3. Configuration Manager Singleton (Metaclass):")
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()
    print(f"config1 is config2: {config1 is config2}")  # Should be True
    
    config1.set_config("debug", True)
    print(f"Debug mode: {config2.get_config('debug')}")
    
    # Test CacheManager singleton
    print("\n4. Cache Manager Singleton (Module-level):")
    cache_manager.set("user_id", 123)
    cache_manager.set("session_token", "abc123")
    print(f"Cached user_id: {cache_manager.get('user_id')}")
    
    # Import the same instance from another part of the code
    from singleton_example import cache_manager as same_cache
    print(f"Same cache instance: {cache_manager is same_cache}")
    print(f"Cached session_token: {same_cache.get('session_token')}")


if __name__ == "__main__":
    demonstrate_singleton() 