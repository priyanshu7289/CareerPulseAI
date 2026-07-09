from auth.auth_service import login_user

success, user = login_user(
    "priyanshu@test.com",
    "Password@123"
)

print(success)

if success and user is not None:
    print(user.full_name)
    print(user.email)