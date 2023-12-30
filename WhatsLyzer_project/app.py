# Libraries Imported
import streamlit as st
import time
import io
import csv
import sys
import seaborn as sns
from custom_modules import func_use_extract_data as func
from custom_modules import func_analysis as analysis
import matplotlib.pyplot as plt
import pandas as pd

# to disable warning by file_uploader going to convert into io.TextIOWrapper
st.set_option('deprecation.showfileUploaderEncoding', False)

# ------------------------------------------------

# Sidebar and main screen text and title.

#--------------------------------------------



senti_title = '<p style="font-family:Times New Roman; color:#ff0066; font-size: 30px;"><U>SENTIMENTAL ANALYSIS</U></p>'

st.sidebar.markdown(senti_title, unsafe_allow_html=True)
#
# data=pd.read_csv("C:/Users/chimu/OneDrive/Desktop/Desktop/Major_Project/WhatsLyzer_minor_project/text.csv", sep='\t')
# data.head()
# data.Sentiment.value_counts()
# Sentiment_count=data.groupby('Sentiment').count()
# plt.bar(Sentiment_count.index.values, Sentiment_count['Phrase'])
# plt.xlabel('Review Sentiments')
# plt.ylabel('Number of Review')
# plt.show()
#







# # --------------------------------------------------------------------------------------------
## SENTIMENTAL - SUBJECTIVITY POLARITY
#
# import csv
# from textblob import TextBlob
#
# infile = "C:/Users/chimu/OneDrive/Desktop/Desktop/Major_Project/WhatsLyzer_minor_project/text.csv"
#
# with open(infile, "r",encoding='utf-8') as csvfile:
#     rows = csv.reader(csvfile)
#     for row in rows:
#         sentence = row[0]
#         blob = TextBlob(sentence)
#         st.markdown(sentence)
#         st.markdown(blob.sentiment.polarity, blob.sentiment.subjectivity)

#------------------------------------------------------------------------------------------









#------------------------------------------------------------------------

#TEXT ANALYSIS

#
#
# from textblob import TextBlob
# import csv
#
#
# df = pd.read_csv("C:/Users/chimu/Downloads/sentence.csv")
#
# #df = pd.DataFrame({'sentence': ['I am very happy', 'I am very sad', 'I am sad but I am happy too']})
#
#
#
# rows = csv.reader(df)
#
# for row in rows:
#     sentence = row[0]
#
# # The x in the lambda function is a row (because I set axis=1)
# # Apply iterates the function accross the dataframe's rows
# df['polarity'] = df.apply(lambda x: TextBlob(x['df']).sentiment.polarity, axis=1)
# df['subjectivity'] = df.apply(lambda x: TextBlob(x['df']).sentiment.subjectivity, axis=1)
#
# st.write(df)
#
#
#
# #feedback="C:/Users/chimu/Downloads/text.csv"
# feedback="thia is cool"
# blob=TextBlob(feedback)
# st.sidebar.markdown(blob.sentiment)

#----------------------------------------------------------------------------------------



st.markdown(""" <style> .reportview-container .markdown-text-container { color: #191970; font-family: Times New Roman; }

</style>
""",
unsafe_allow_html = True
)


original_title = '<p style="font-family:Times New Roman; color:#FFFAF0; font-size: 70px;"><U>WHATSLYZER</U></p>'


st.markdown(original_title, unsafe_allow_html=True)

# st.title(" ")

st.markdown(
            """
            <style>
            .reportview-container {
                background-color: #20B2AA
            }
           # .sidebar .sidebar-content {
           #      background: url("https://image.shutterstock.com/image-vector/stats-pulse-logo-design-template-260nw-1068801485.jpg")
           #  }
            </style>
            """,
            unsafe_allow_html=True
        )

import streamlit as st
import base64

LOGO_IMAGE = "C:/Users/chimu/OneDrive/Desktop/Desktop/Major_Project/WhatsLyzer_minor_project/images/stats-pulse.jpg"

st.markdown(
    """
    <style>
    .container {
        display: flex;
    }
    .logo-text {
        font-weight:100 !important;
        font-size:20px !important;
        color: #f9a01b !important;
        padding-top: 50px !important;
    }
    .logo-img {
        float:right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">

    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown('**Upload Chat File Here !!!!:**')

date_format = st.sidebar.selectbox('Please select the date format of your file:',
                                 ('mm/dd/yyyy', 'mm/dd/yy',
                                  'dd/mm/yyyy', 'dd/mm/yy',
                                  'yyyy/mm/dd', 'yy/mm/dd'), key='0')
filename = st.sidebar.file_uploader("", type=["txt"])


# =========================================================

# Select feature for txt file {Way 2}

# def file_selector(folder_path='.'):
#     filenames = os.listdir(folder_path)
#     selected_filename = st.sidebar.selectbox('Select a file', filenames)
#     return os.path.join(folder_path, selected_filename)

# filename = file_selector()
# st.sidebar.markdown('You selected {}'.format(filename))

# Check file format
# if not filename.endswith('.txt'):
#     st.error("Please upload only text file!")
#     st.sidebar.error("Please upload only text file!")  
# else:

# ===========================================================
if filename is not None:

    # Loading files into data as a DataFrame
    # filename = ("./Chat.txt")
    
    @st.cache(persist=True, allow_output_mutation=True)
    def load_data(date_format=date_format):
        
        reader = csv.reader(filename, delimiter='\n')
        file_contents = []
        
        for each in reader:
            if len(each) > 0:
                file_contents.append(each[0])
            else:
                file_contents.append('')

        return func.read_data(file_contents, date_format)
    
    try:
        data = load_data()
        
        if data.empty:
            st.error("Please upload the WhatsApp chat dataset!")
            
        # if st.sidebar.checkbox("Show raw data", False):
        #     st.write(data)
        # ------------------------------------------------

        st.sidebar.title('**RESULT...**')

        st.sidebar.write(analysis.senti(data))








        # Members name involve in Chart
        st.sidebar.markdown("### To Analyze Select Below:")
        names = analysis.authors_name(data)
        names.append('All')
        member = st.sidebar.selectbox("Member Name", names, key='1')
        # selected_user = st.sidebar.selectbox("Show analysis wrt",data)

        if not st.sidebar.checkbox("Hide", True):

            try:


                import getpass

                database = {"Vanshika": "123456", "minor": "project"}
                username = input("Enter Your Username : ")
                password = getpass.getpass("Enter Your Password : ")
                for i in database.keys():
                    if username == i:
                        while password != database.get(i):
                            password = getpass.getpass("Enter Your Password Again : ")
                        break
                print("Verified")


                if member == "All":
                    st.title("Analyze __{}__ members together:".format(member))
                    st.markdown(analysis.stats(data), unsafe_allow_html=True)


                    st.title("**Top 10 frequent use emoji:**")

                    emoji = analysis.popular_emoji(data)
                    for e in emoji[:10]:

                        st.markdown('**{}** : {}'.format(e[0], e[1]))

                    st.title('**Visualize emoji distribution in pie chart:**')
                    st.plotly_chart(analysis.visualize_emoji(data))

                    st.title('**Word Cloud:**')
                    st.text("This will show the cloud of words which you use, larger the word size most often you use.")
                    st.pyplot(analysis.word_cloud(data))
                    # st.pyplot()

                    time.sleep(0.2)

                    st.title('**Most active date:**')
                    st.pyplot(analysis.active_date(data))
                    # st.pyplot()

                    time.sleep(0.2)

                    st.title('**Most active time for chat:**')
                    st.pyplot(analysis.active_time(data))
                    # st.pyplot()

                    st.title('**Day wise distribution of messages for {}:**'.format(member))
                    st.plotly_chart(analysis.day_wise_count(data))



                    # st.write('**??:**')
                    # st.plotly_chart(analysis.activity_heatmap(selected_user,data))
                    #

                    st.title('**Number of messages as times move on**')
                    st.plotly_chart(analysis.num_messages(data))

                    # st.write('**user**')
                    # st.plotly_chart(analysis.user_chat_pie(data))


                    st.title('**Chatter:**')
                    st.plotly_chart(analysis.chatter(data))



                else:



                    member_data = data[data['Author'] == member]
                    st.title("Analyze {} chat:".format(member))
                    st.markdown(analysis.stats(member_data), unsafe_allow_html=False)

                    st.title("**Top 10 Popular emoji:**")
                    emoji = analysis.popular_emoji(member_data)
                    for e in emoji[:10]:
                        st.markdown('**{}** : {}'.format(e[0], e[1]))

                    st.title('**Visualize emoji distribution in pie chart:**')
                    st.plotly_chart(analysis.visualize_emoji(member_data))

                    st.title('**Word Cloud:**')
                    st.text("This will show the cloud of words which you use, larger the word size most often you use.")
                    st.pyplot(analysis.word_cloud(member_data))

                    time.sleep(0.2)

                    st.title('**Most active date of {} on WhatsApp:**'.format(member))
                    st.pyplot(analysis.active_date(member_data))
                    # st.pyplot()

                    time.sleep(0.2)

                    st.title('**When {} is active for chat:**'.format(member))
                    st.pyplot(analysis.active_time(member_data))
                    # st.pyplot()

                    st.title('**Day wise distribution of messages for {}:**'.format(member))
                    st.plotly_chart(analysis.day_wise_count(member_data))

                    st.title('**Number of messages as times move on**')
                    st.plotly_chart(analysis.num_messages(member_data))



                    st.title('**Chatter:**')
                    st.plotly_chart(analysis.chatter(member_data))


            except:
                e = sys.exc_info()[0]
                st.error("It seems that something is wrong! Try Again. Error Type: {}".format(e.__name__))

        # --------------------------------------------------

    except:
        e = sys.exc_info()[0]
        st.error("Something is wrong in loading the data! Please select the correct date format or Try again. Error Type: {}".format(e.__name__))
