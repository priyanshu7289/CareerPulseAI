from auth.auth_service import register_user

success, message = register_user(
    full_name="Priyanshu Kumar",
    email="priyanshu@test.com",
    password="Password@123",
    target_role="Data Analyst"
)

print(success)
print(message)