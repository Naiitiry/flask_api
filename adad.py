from werkzeug.security import generate_password_hash

password = "Plaza133!"
password_hash = generate_password_hash(password)
print(password_hash)
