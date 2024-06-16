import random
import string


def generate_random_user():
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(8))
    last_name = ''.join(random.choice(letters) for i in range(8))
    email = ''.join(random.choice(letters) for i in range(8)) + '@mymail.com'
    password = ''.join(random.choice(letters + string.digits) for i in range(10))

    return name, last_name, email, password
