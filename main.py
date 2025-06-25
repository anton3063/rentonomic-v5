import os

print("DEBUG: Checking environment variables...")
required_vars = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "CLOUDINARY_CLOUD_NAME",
    "CLOUDINARY_API_KEY",
    "CLOUDINARY_API_SECRET",
]

missing_vars = []
for var in required_vars:
    value = os.getenv(var)
    if value is None:
        print(f"DEBUG: {var} is MISSING!")
        missing_vars.append(var)
    elif value.strip() == "":
        print(f"DEBUG: {var} is EMPTY or whitespace!")
        missing_vars.append(var)
    else:
        print(f"DEBUG: {var} is set to: '{value[:4]}...'")  # show first 4 chars only for privacy

if missing_vars:
    raise RuntimeError(f"One or more environment variables are missing or empty: {missing_vars}")
else:
    print("DEBUG: All required environment variables are set correctly.")






















   



