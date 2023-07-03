from app import bcrypt


def main(password):
    pass_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    return pass_hash


if __name__ == "__main__":
    print(main("admin"))
