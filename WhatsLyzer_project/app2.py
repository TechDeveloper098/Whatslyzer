# Libraries Imported
import streamlit as st
import docx2txt
import io
import csv
import sys
import seaborn as sns
from custom_modules import func_use_extract_data as func
from custom_modules import func_analysis as analysis
import matplotlib.pyplot as plt
import pandas as pd
import sys
import subprocess
# Libraries Imported
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import nltk
# nltk.download()
import re
import numpy as np
from textblob import TextBlob


# to disable warning by file_uploader going to convert into io.TextIOWrapper
st.set_option('deprecation.showfileUploaderEncoding', False)



# ------------------------------------------------

# Sidebar and main screen text and title.

# --------------------------------------------


st.markdown(""" <style> .reportview-container .markdown-text-container { color: #191970; font-family: Times New Roman; }

</style>
""",
            unsafe_allow_html=True
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


if not st.sidebar.checkbox("Whatsapp chat analysis", True):


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


        # st.sidebar.markdown("Enter the Credentials")
        # st.markdown(analysis.check(data))

        try:
            data = load_data()

            if data.empty:
                st.error("Please upload the WhatsApp chat dataset! or Decrypt your file first!!! ")

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

            # if not st.sidebar.checkbox("Hide", True):

                # try:

                    # import getpass
                    #
                    # database = {"Vanshika": "123456", "minor": "project"}
                    # username = input("Enter Your Username : ")
                    # password = getpass.getpass("Enter Your Password : ")
                    # for i in database.keys():
                    #     if username == i:
                    #         while password != database.get(i):
                    #             password = getpass.getpass("Enter Your Password Again : ")
                    #         break
                    # print("Verified")

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

        # except:
        #     e = sys.exc_info()[0]
        #     st.error(
        #         "Something is wrong in loading the data! Please select the correct date format or Try again. Error Type: {}".format(
        #             e.__name__))

#-----------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------

if not st.sidebar.checkbox("Sentimental Analysis", True):

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

    senti_title = '<p style="font-family:Times New Roman; text-align: center; color:#ff0066; font-size: 40px;"><U>SENTIMENTAL ANALYSIS</U></p>'

    st.markdown(senti_title, unsafe_allow_html=True)

    # def senti(data):

    # to disable warning by file_uploader going to convert into io.TextIOWrapper
    st.set_option('deprecation.showfileUploaderEncoding', False)

    #
    # file = open('C:/Users/chimu/OneDrive/Desktop/Desktop/7th sem/minor_project/ddmmyyyyWhatsApp Chat with CSE-B (Students) (1).txt',
    #             encoding="utf-8-sig");  # Encoding removes the byte order mark at beginning of text
    #

    uploaded_file = st.sidebar.file_uploader("Add text file !")
    if uploaded_file:
        for line in uploaded_file:

            # st.write(line)

            t = uploaded_file.read()





            polar_title = '<p style="font-family:Times New Roman; color:#BE20C3; font-size: 30px;"><U>POLARITY</U></p>'

            st.sidebar.markdown(polar_title, unsafe_allow_html=True)

            polar_write = '<p style="font-family:Times New Roman; color:#208CC3; font-size: 18px;">If Ploarity is greater than zero so teh statement is positive . Polarity measure will tell you how positive or negative  your statement is</p>'

            st.sidebar.markdown(polar_write, unsafe_allow_html=True)

            polar_title = '<p style="font-family:Times New Roman; color:#BE20C3; font-size: 30px;"><U>SUBJECTIVITY</U></p>'

            st.sidebar.markdown(polar_title, unsafe_allow_html=True)

            polar_write = '<p style="font-family:Times New Roman; color:#208CC3; font-size: 18px;">Subjectivity expresses about personal feelings views or belief. Generally refer to personal opinion, emotion or judgement whereas objective refers to factual information. Subjectivity is also a float which lies in the range of [0,1].</p>'

            st.sidebar.markdown(polar_write, unsafe_allow_html=True)





            # Clean up text file for better analysis

            # Remove extra text that does not have to do with the actual novel, e.g. Project Gutenberg text at beginning and end of file
            # Cleaning up the text file by deleting or replacing characters that causes issues with TextBlob
            t = t.replace('“', '');  # Quotes cause issues because they 'combine sentences'
            t = t.replace('”', '');
            t = t.replace('_', '');  # Underscores signify italicization, remove them.

            # Finds all chapter headings and creates 'sentences' out of them so they are not combined with other sentences
            # This is done because there is no period at the end of the chapter declaration, e.g. Chapter 1 instead of Chapter 1.
            # This in turn causes TextBlob to combine the chapter declaration with the next sentence since it sees now punctuation

            # Regex to find matches of Chapter + Number + Space. The space is needed so it doesn't confuse Chapter 1 with Chapter 10, 11, 12 etc...
            matches = re.findall('Chapter ' + '\d{1,2}\s', t)  # 'Chapter' + 1-2 digits \d{1,2} + space \s
            print(matches)
            for match in matches:  # Cycles through matches in order to find them and replace them with itself + period to create new sentence
                t = re.sub(match, match.replace('\n', '.'), t)

            t = t.replace('\n', ' ');  # Replace newline with space
            blob = TextBlob(t)  # Pass in clean text file to TextBlob

            # -----------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------
            # Create Pandas DataFrame to store data
            df = pd.DataFrame(
                columns=['Sentence', 'Polarity', 'Subjectivity'])
            sentencecount = 0  # Counter for sentences
            # totalwords = {}  # Empty dictionary for keeping track of unique words
            # propernouns = {}  # Empty dictionary for keeping track of unique proper nouns

            # Cycling through all the sentences in the text file
            for sentence in blob.sentences:
                # # Counters for nouns, verbs, and adjectives in current sentence
                # nouns = 0
                # verbs = 0
                # adjectives = 0
                #

                # Printing pertinent information
                newsent_title = '<p style="font-family:Times New Roman; color:#145A32; text-align: center; font-size: 20px;"><U>New sentence</U></p>'

                st.markdown(newsent_title, unsafe_allow_html=True)
                # st.markdown(sentencecount)
                title = '<p style="font-family:Times New Roman; color:#ff8000; font-size: 15px;">Current Sentence - </p>'

                st.markdown(title, unsafe_allow_html=True)
                st.markdown(sentence)  # Current sentence
                polarity = '<p style="font-family:Times New Roman; color: red; font-size: 17px;">Polarity</p>'

                st.markdown(polarity, unsafe_allow_html=True)
                st.markdown(sentence.sentiment.polarity)  # Current sentence polarity
                subjectivity = '<p style="font-family:Times New Roman; color: red; font-size: 17px;">Subjectivity</p>'

                st.markdown(subjectivity, unsafe_allow_html=True)

                st.markdown(sentence.sentiment.subjectivity)  # Current sentence subjectivity

                # st.markdown(sentence.tags)  # Current sentence words and their part of speech (POS) tag

                # Entering data into dataframe
                df.at[sentencecount, 'Sentence'] = str(sentence)
                # df.at[sentencecount, 'Tags'] = str(sentence.tags)
                df.at[sentencecount, 'Polarity'] = sentence.sentiment.polarity
                df.at[sentencecount, 'Subjectivity'] = sentence.sentiment.subjectivity

                df.to_csv('Sentiment Analysis.csv')

                # Histogram charts for text file
                fig5, (ax18, ax19) = plt.subplots(2)
                fig5.subplots_adjust(hspace=.5)

                h = sorted(df['Polarity'])
                ax18.hist(h, bins='auto', color='tab:blue')
                ax18.set_title('Polarity $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
                ax18.set_ylabel('Number of Occurrences', color='tab:blue')
                ax18.tick_params('y', color='tab:blue')

                h = sorted(df['Subjectivity'])
                ax19.hist(h, bins='auto', color='tab:blue')
                ax19.set_title('Subjectivity $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
                ax19.set_ylabel('Number of Occurrences', color='tab:blue')
                ax19.tick_params('y', color='tab:blue')
                st.pyplot(fig5)






