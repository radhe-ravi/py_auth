import bcrypt

def generate_hash_password(password):
    salt = bcrypt.gensalt(4)
    hashed = bcrypt.hashpw(password.encode('utf-8'),salt)
    return hashed.decode('utf-8')

def verify_password_with_hashed_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8') , hashed_password.encode('utf-8'))