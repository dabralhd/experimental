# error_types.py
from enum import Enum

class ErrorType(Enum):
    FILE_NOT_FOUND = "File not found"
    PERMISSION_DENIED = "Permission denied"
    CONNECTION_TIMEOUT = "Connection timeout"
    INVALID_INPUT = "Invalid input"
    RESOURCE_LIMIT_EXCEEDED = "Resource limit exceeded"
    CPU_LIMIT_EXCEEDED = "CPU limit exceeded"
    RAM_LIMIT_EXCEEDED = "Memory RAM limit exceeded"
    JOB_LIMIT_EXCEEDED = "JOB limit exceeded"
    DISK_LIMIT_EXCEEDED = "Disk Space limit exceeded"
    UNKNOWN_ERROR = "Unknown error"

# Example usage
def handle_error(error_type: ErrorType):
    if error_type == ErrorType.FILE_NOT_FOUND:
        print("Error: The specified file could not be found.")
    elif error_type == ErrorType.PERMISSION_DENIED:
        print("Error: You do not have the necessary permissions.")
    elif error_type == ErrorType.CONNECTION_TIMEOUT:
        print("Error: The connection has timed out.")
    elif error_type == ErrorType.INVALID_INPUT:
        print("Error: The input provided is invalid.")
    elif error_type == ErrorType.RESOURCE_LIMIT_EXCEEDED:
        print("Error: Some resource limit has been exceeded.")
    elif error_type == ErrorType.CPU_LIMIT_EXCEEDED:
        print("Error: The CPU limit has been exceeded.")
    elif error_type == ErrorType.RAM_LIMIT_EXCEEDED:
        print("Error: The RAM limit has been exceeded.")
    elif error_type == ErrorType.JOB_LIMIT_EXCEEDED:
        print("Error: The Job limit has been exceeded.")
    elif error_type == ErrorType.DISK_LIMIT_EXCEEDED:
        print("Error: The Disk limit has been exceeded.")    
    elif error_type == ErrorType.UNKNOWN_ERROR:
        print("Error: An unknown error has occurred.")
    else:
        print("Error: Unhandled error type.")
