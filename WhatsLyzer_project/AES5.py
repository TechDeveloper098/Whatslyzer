import os
import hashlib
import sys
import base64
import threading
import time

from getpass import getpass
from cryptography.fernet import Fernet

global threads
threads = []


class Cryptor:
    def __init__(self, password):
        self.__password = password

    def operate(self, file_):
        global threads
        if file_.endswith("enc"):
            t = threading.Thread(target=self.decrypt, args=(file_,), daemon=True)
            t.start()
            threads.append(t)
        else:
            t = threading.Thread(target=self.encrypt, args=(file_,), daemon=True)
            t.start()
            threads.append(t)

    def _get_fernet_instance(self, salt):
        key = base64.urlsafe_b64encode(hashlib.pbkdf2_hmac("sha256",
                                                           bytes(self.__password, encoding="utf-8"),
                                                           salt,
                                                           100000,
                                                           dklen=32))
        return Fernet(key)

    def decrypt(self, file_):
        file_name = os.path.splitext(file_)[0]

        with open(file_, "rb") as _file_:
            data = _file_.readline()
            encrypted_file_ext = _file_.readline()
            salt = b"".join(_file_.readlines())

            f = self._get_fernet_instance(salt)
            decrypted = f.decrypt(data)
            file_ext = f.decrypt(encrypted_file_ext)

        with open(file_name + file_ext.decode(encoding="utf-8"), "wb") as _file_:
            _file_.write(decrypted)

        os.remove(file_)

    def encrypt(self, file_):
        salt = os.urandom(32)
        f = self._get_fernet_instance(salt)
        file_name, file_ext = os.path.splitext(file_)

        with open(file_, "rb") as _file_:
            file__ = _file_.read()
            encrypted = f.encrypt(bytes(file__))
            encrypted_file_ext = f.encrypt(bytes(file_ext, encoding="utf-8"))

        with open(f"{file_name}.enc", "wb") as _file_:
            _file_.write(encrypted + b"\n" + encrypted_file_ext + b"\n" + salt)

        os.remove(file_)


def iterate(crypt, file_):
    if os.path.isdir(file_):
        files = []
        for dirpath, dirname, filename in os.walk(file_):
            for dir_ in dirname:
                files.append(dirpath + "/" + dir_)
            for file_name in filename:
                files.append(dirpath + "/" + file_name)
            break

        for file_ in files:
            iterate(crypt, file_)
    else:
        crypt.operate(file_)


def main():
    files = sys.argv[1:]
    password = getpass("Password:")
    re_password = getpass("Confirm Password:")
    if password != re_password:
        print("Passwords don't match")
        return
    crypt = Cryptor(password)

    for file_ in files:
        iterate(crypt, file_)


if __name__ == "__main__":
    time1 = time.time()
    main()

    while True:
        for x in threads:
            if x.is_alive():
                time.sleep(0.5)
                break
        else:
            break

    print(f"Completed in {round(time.time() - time1, 4)}")