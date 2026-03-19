import math

# A "Secret" salt that should not be visible in plain text.
# In a real app, this might be a key for HMAC or an encryption seed.
SECRET_SALT = 0.731928465

def calculate_secure_hash(input_value):
    """
    Complex math to obfuscate business logic.
    This simulates a proprietary algorithm that calculates a 
    pseudo-hash using trigonometry and logarithmic scaling.
    """
    # Defensive check: ensure we don't take log of zero
    assert input_value != 0, "Input cannot be zero for this algorithm"

    # Step 1: Combine input with Pi and apply sine transformation
    step1 = math.sin(input_value) * math.pi
    
    # Step 2: Incorporate the secret salt and apply a natural log
    # The salt is 'baked' into the result here
    step2 = math.log(abs(step1 + SECRET_SALT))
    
    # Step 3: Final non-linear transformation
    result = (step2 ** 2) / math.sqrt(abs(input_value))
    
    return round(result, 5)

if __name__ == "__main__":
    # Test values to demonstrate the logic
    test_inputs = [10, 42, 100]
    
    print("--- Secure Logic Demonstration ---")
    for val in test_inputs:
        output = calculate_secure_hash(val)
        print(f"Input: {val} | Computed Result: {output}")