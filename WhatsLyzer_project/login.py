import streamlit as st
import subprocess
from PIL import Image


title = '<p style="font-family:Times New Roman; color:#FFFAF0; font-size: 20px;">Login with correct credentials</p>'

image = Image.open('C:/Users/chimu/OneDrive/Desktop/Desktop/Major_Project/WhatsLyzer_minor_project/images/login.jpg')

st.image(image,width=550,height=300)




st.markdown(
            """
            <style>
            .reportview-container {
                background-color: #1B4F72 
            }
          
            </style>
            """,
            unsafe_allow_html=True
        )

import getpass
import os
# if st.button('Login'):
# #
#     database = {"Vanshika": "123456", "minor": "project"}
#     username = input("Enter Your Username : ")
#     password = getpass.getpass("Enter Your Password : ")
#     for i in database.keys():
#         if username == i:
#             while password != database.get(i):
#                 password = getpass.getpass("Enter Your Password Again : ")
#             break
#
#
#     st.markdown("Verified")

process = subprocess.Popen(["streamlit", "run", os.path.join('C:/Users/chimu/.spyder-py3/example.py')])

    #     'C:/Users/chimu/OneDrive/Desktop/Desktop/Major_Project/WhatsLyzer_minor_project/app2.py')])
    # # os.system('C:/Users/chimu/OneDrive/Desktop/Desktop/Major_Project/WhatsLyzer_minor_project/app2.py')

#
# else:
#     st.markdown(title, unsafe_allow_html=True)
#
