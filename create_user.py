import bcrypt

password = "tren"

hashed = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
)

print(hashed.decode())