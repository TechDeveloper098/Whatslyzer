from Crypto.Cipher import AES
from secrets import token_bytes
import streamlit as st
key = token_bytes(16)

st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.sidebar.file_uploader("Add text file !")
# if uploaded_file:
#     for line in uploaded_file:
#         t = uploaded_file.read()


def encrypt(msg):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    # ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))

    ciphertext, tag = cipher.encrypt_and_digest(msg.encode())
    return nonce, ciphertext, tag

def decrypt(nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        return plaintext.decode()
    except:
        return False


# nonce, ciphertext, tag = encrypt(open(uploaded_file))




nonce, ciphertext, tag = encrypt(uploaded_file)


st.markdown("encrypted successfully")
plaintext = decrypt(nonce, ciphertext, tag)
st.markdown(f'Cipher text: {ciphertext}')
if not plaintext:
    st.markdown('Message is corrupted')
else:

    st.markdown(f'Plain text: {plaintext}')