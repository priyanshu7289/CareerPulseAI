from auth.password import hash_password, verify_password

password = "Priyanshu123"

hashed = hash_password(password)

print(hashed)

print(verify_password(password, hashed))