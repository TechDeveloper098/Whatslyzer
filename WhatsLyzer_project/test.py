
# Libraries Imported
import streamlit as st
import time
import io
import csv
import sys
import seaborn as sns
# from custom_modules import func_use_extract_data as func
# from custom_modules import func_analysis as analysis
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




st.markdown(
            """
            <style>
            .reportview-container {
                background-color: #99F0FA
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


polar_title = '<p style="font-family:Times New Roman; color:#BE20C3; font-size: 30px;"><U>POLARITY</U></p>'

st.sidebar.markdown(polar_title, unsafe_allow_html=True)

polar_write = '<p style="font-family:Times New Roman; color:#208CC3; font-size: 18px;">If Ploarity is greater than zero so teh statement is positive . Polarity measure will tell you how positive or negative  your statement is</p>'

st.sidebar.markdown(polar_write, unsafe_allow_html=True)



polar_title = '<p style="font-family:Times New Roman; color:#BE20C3; font-size: 30px;"><U>SUBJECTIVITY</U></p>'

st.sidebar.markdown(polar_title, unsafe_allow_html=True)

polar_write = '<p style="font-family:Times New Roman; color:#208CC3; font-size: 18px;">Subjectivity expresses about personal feelings views or belief. Generally refer to personal opinion, emotion or judgement whereas objective refers to factual information. Subjectivity is also a float which lies in the range of [0,1].</p>'

st.sidebar.markdown(polar_write, unsafe_allow_html=True)





#
# file = open('C:/Users/chimu/OneDrive/Desktop/Desktop/7th sem/minor_project/ddmmyyyyWhatsApp Chat with CSE-B (Students) (1).txt',
#             encoding="utf-8-sig");  # Encoding removes the byte order mark at beginning of text
#

uploaded_file = st.file_uploader("Add text file !")
if uploaded_file:
    for line in uploaded_file:

        # st.write(line)


        t = uploaded_file.read()



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



        #-----------------------------------------------------------------------------
        #----------------------------------------------------------------------------------
        # Create Pandas DataFrame to store data
        df = pd.DataFrame(
            columns=['Sentence', 'Polarity', 'Subjectivity'])
        sentencecount = 0  # Counter for sentences
        #totalwords = {}  # Empty dictionary for keeping track of unique words
        #propernouns = {}  # Empty dictionary for keeping track of unique proper nouns

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
            #st.markdown(sentencecount)
            title = '<p style="font-family:Times New Roman; color:#ff8000; font-size: 15px;">Current Sentence - </p>'

            st.markdown(title, unsafe_allow_html=True)
            st.markdown(sentence)  # Current sentence
            polarity ='<p style="font-family:Times New Roman; color: red; font-size: 17px;">Polarity</p>'

            st.markdown(polarity,unsafe_allow_html=True)
            st.markdown(sentence.sentiment.polarity)  # Current sentence polarity
            subjectivity = '<p style="font-family:Times New Roman; color: red; font-size: 17px;">Subjectivity</p>'

            st.markdown(subjectivity, unsafe_allow_html=True)

            st.markdown(sentence.sentiment.subjectivity)  # Current sentence subjectivity

            #st.markdown(sentence.tags)  # Current sentence words and their part of speech (POS) tag

            # Entering data into dataframe
            df.at[sentencecount, 'Sentence'] = str(sentence)
            #df.at[sentencecount, 'Tags'] = str(sentence.tags)
            df.at[sentencecount, 'Polarity'] = sentence.sentiment.polarity
            df.at[sentencecount, 'Subjectivity'] = sentence.sentiment.subjectivity

            df.to_csv('Sentiment Analysis.csv')

            # Histogram charts for text file
            fig5,(ax18, ax19) = plt.subplots(2)
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














#------------------------------------------------------------------------------------------
#     df.at['Average Polarity'] = df.loc[value + 1:, 'Polarity'].mean()
#     df.at['Average Subjectivity'] = df.loc[value + 1:, 'Subjectivity'].mean()
#
#     fig3, (ax10, ax11) = plt.subplots(2)
#     fig3.subplots_adjust(hspace=.5)
#     h = sorted(df['Average Polarity'])
#     ax10.hist(h, bins='auto', color='tab:blue')
#     ax10.set_title(
#         'Avg. Polarity per Chapter $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
#     ax10.set_ylabel('Number of Occurrences', color='tab:blue')
#     ax10.tick_params('y', color='tab:blue')
#
#     h = sorted(df['Average Subjectivity'])
#     ax11.hist(h, bins='auto', color='tab:blue')
#     ax11.set_title(
#         'Avg. Subjectivity per Chapter $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
#     ax11.set_ylabel('Number of Occurrences', color='tab:blue')
#     ax11.tick_params('y', color='tab:blue')
#
#     st.pyplot(fig3)
# #------------------------------------------------------------------------------------------------
    #df.at[sentencecount, 'Number of Words'] = len(sentence.words)

    # Cycling through every word in current sentence
    # for word in sentence.tags:
    #
    #     # Checks if current word is in the unique word dictionary
    #     if word not in totalwords:  # If not, adds it to unique word dictonary with value of 1 (first appearance)
    #         totalwords[word] = 1
    #     else:  # If it is, adds 1 to its value for subsequent appearances
    #         totalwords[word] += 1
    #
    #     # List of tags https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    #
    #     if word[1] == 'NNP':  # Checks if current word is proper noun so it can add it to the proper noun dictionary
    #         if word not in propernouns:
    #             propernouns[word] = 1
    #         else:
    #             propernouns[word] += 1
    #
    #     # Cheks if current word is a noun, verb, or adjective so it can add to the corresponding count
    #     if word[1] == 'NN' or word[1] == 'NNS':
    #         nouns += 1
    #     if word[1] == 'VB' or word[1] == 'VBD' or word[1] == 'VBG' or word[1] == 'VBN' or word[1] == 'VBP' or word[
    #         1] == 'VBZ':
    #         verbs += 1
    #     if word[1] == 'JJ' or word[1] == 'JJR' or word[1] == 'JJS':
    #         adjectives += 1
    #
    # # Entering word count data into dataframe
    # df.at[sentencecount, 'Number of Nouns'] = nouns
    # df.at[sentencecount, 'Number of Verbs'] = verbs
    # df.at[sentencecount, 'Number of Adjectives'] = adjectives
    #
    # # Counter for sentences
    # sentencecount += 1

# Saves dataframe to csv file

#
# st.markdown(
#     '------------------------------------------------Text Information------------------------------------------------')
# st.markdown(df.head())
# st.markdown('Total Number of Sentences: ', sentencecount)
# st.markdown('Total Number of Words: ',
#       df['Number of Words'].sum() - 61 * 2)  # -61*2 because of 61 chapters and 2 words Chapter and ##
# st.markdown('Total Number of Nouns: ', df['Number of Nouns'].sum() - 61)  # -61 because of 61 chapters, chapter is a noun
# st.markdown('Total Number of Verbs: ', df['Number of Verbs'].sum())
# st.markdown('Total Number of Adjectives: ', df['Number of Adjectives'].sum())
# st.markdown('Total Number of Unique Words: ', len(totalwords))
# st.markdown('Total Number of Unique Proper Nouns: ', len(propernouns))
#
# # Calculating 20 most used words and proper nouns
# tw = dict(Counter(totalwords).most_common(20))
# st.markdown('Twenty most used words: ', tw)
#
# # Deleting certain proper nouns from dictionary
# propernouns.pop(('Mr.', 'NNP'))
# propernouns.pop(('Mrs.', 'NNP'))
# propernouns.pop(('Lady', 'NNP'))
# propernouns.pop(('Miss', 'NNP'))
# propernouns.pop(('Colonel', 'NNP'))
# propernouns.pop(('Sir', 'NNP'))
#
# pn = dict(Counter(propernouns).most_common(20))
# st.markdown('Twenty most used Proper nouns: ', pn)
#
# # Bar Chart for 20 most used words
# fig, ax0 = plt.subplots(figsize=(19.2, 10.8))
#
# ax0.bar(range(len(tw)), list(tw.values()), align='center')
# ax0.set_title('Most Used  Words')
# ax0.set_xlabel('Word and Tag')
# ax0.set_ylabel('Word Count')
# plt.xticks(range(len(tw)), list(tw.keys()), rotation=90)
#
# fig.savefig('Word_Count.png', bbox_inches="tight")
#
# # Bar Chart for 20 most used proper ouns
# fig1, ax1 = plt.subplots(figsize=(19.2, 10.8))
#
# ax1.bar(range(len(pn)), list(pn.values()), align='center')
# ax1.set_title('Most Used Proper nouns')
# ax1.set_xlabel('Word and Tag')
# ax1.set_ylabel('Word Count')
# plt.xticks(range(len(pn)), list(pn.keys()), rotation=90)
#
# fig1.savefig('Proper_noun_Count.png', bbox_inches="tight")

# h = sorted(df['Number of Words'])
# ax20.hist(h, bins='auto', color='tab:blue')
# ax20.set_title('Number of Words $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax20.set_ylabel('Number of Occurrences', color='tab:blue')
# ax20.tick_params('y', color='tab:blue')
#
# h = sorted(df['Number of Nouns'])
# ax21.hist(h, bins='auto', color='tab:blue')
# ax21.set_title('Number of Nouns $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax21.set_ylabel('Number of Occurrences', color='tab:blue')
# ax21.tick_params('y', color='tab:blue')
#
# h = sorted(df['Number of Verbs'])
# ax22.hist(h, bins='auto', color='tab:blue')
# ax22.set_title('Number of Verbs $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax22.set_ylabel('Number of Occurrences', color='tab:blue')
# ax22.tick_params('y', color='tab:blue')
#
# h = sorted(df['Number of Adjectives'])
# ax23.hist(h, bins='auto', color='tab:blue')
# ax23.set_title('Number of Adjectives $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax23.set_ylabel('Number of Occurrences', color='tab:blue')
# ax23.tick_params('y', color='tab:blue')

# fig5.savefig('Histogram for Text File.png', bbox_inches="tight")
#--------------------------------------------------------------------------
#------------------------------------------------------------------------------







#
# print('----------------------------------------------Chapter Information----------------------------------------------')
# # Cycles through chapters to acquire row index in dataframe for that chapter
# chapters = {}
# for match in matches:
#     print(match.replace('\n', '.'), df.loc[df['Sentence'] == match.replace('\n', '.')].index.values)
#     chapters[match.replace('\n', '.')] = int(df.loc[df['Sentence'] == match.replace('\n', '.')].index.values)
# ch_list = list(chapters.items())
#
# # Creating new dataframe for chapter specific data
# df_ch = pd.DataFrame(columns=['Chapter',
#                               'Number of Sentences',
#                               'Average Polarity',
#                               'Average Subjectivity',
#                               'Total Number of Words',
#                               'Average Number of Words',
#                               'Total Number of Nouns',
#                               'Average Number of Nouns',
#                               'Total Number of Verbs',
#                               'Average Number of Verbs',
#                               'Total Number of Adjectives',
#                               'Average Number of Adjectives',
#                               ])
#
# # Cycles through original dataframe with row indices for each chapter in order to calculate means of each chapter
# for i, (key, value) in enumerate(chapters.items()):
#     print(i, key, value)
#
#     if i < len(ch_list) - 1:  # All chapters except last chapter
#         df_ch.at[i, 'Chapter'] = key
#         df_ch.at[i, 'Number of Sentences'] = ch_list[i + 1][1] - 1 - value
#         df_ch.at[i, 'Average Polarity'] = df.loc[value + 1:ch_list[i + 1][1] - 1, 'Polarity'].mean()
#         df_ch.at[i, 'Average Subjectivity'] = df.loc[value + 1:ch_list[i + 1][1] - 1, 'Subjectivity'].mean()
#         df_ch.at[i, 'Total Number of Words'] = df.loc[value + 1:ch_list[i + 1][1] - 1, 'Number of Words'].sum()
#         df_ch.at[i, 'Average Number of Words'] = df.loc[value + 1:ch_list[i + 1][1] - 1, 'Number of Words'].mean()
#         df_ch.at[i, 'Total Number of Nouns'] = df.loc[value + 1:ch_list[i + 1][1] - 1, 'Number of Nouns'].sum()
#         df_ch.at[i, 'Average Number of Nouns'] = df.loc[value + 1:ch_list[i + 1][1] - 1, 'Number of Nouns'].mean()
#         df_ch.at[i, 'Total Number of Verbs'] = df.loc[value + 1:ch_list[i + 1][1] - 1, 'Number of Verbs'].sum()
#         df_ch.at[i, 'Average Number of Verbs'] = df.loc[value + 1:ch_list[i + 1][1] - 1, 'Number of Verbs'].mean()
#         df_ch.at[i, 'Total Number of Adjectives'] = df.loc[value + 1:ch_list[i + 1][1] - 1,
#                                                     'Number of Adjectives'].sum()
#         df_ch.at[i, 'Average Number of Adjectives'] = df.loc[value + 1:ch_list[i + 1][1] - 1,
#                                                       'Number of Adjectives'].mean()
#     else:  # Last chapter
#         df_ch.at[i, 'Chapter'] = key
#         df_ch.at[i, 'Number of Sentences'] = sentencecount - 1 - value
#         df_ch.at[i, 'Average Polarity'] = df.loc[value + 1:, 'Polarity'].mean()
#         df_ch.at[i, 'Average Subjectivity'] = df.loc[value + 1:, 'Subjectivity'].mean()
#         df_ch.at[i, 'Total Number of Words'] = df.loc[value + 1:, 'Number of Words'].sum()
#         df_ch.at[i, 'Average Number of Words'] = df.loc[value + 1:, 'Number of Words'].mean()
#         df_ch.at[i, 'Total Number of Nouns'] = df.loc[value + 1:, 'Number of Nouns'].sum()
#         df_ch.at[i, 'Average Number of Nouns'] = df.loc[value + 1:, 'Number of Nouns'].mean()
#         df_ch.at[i, 'Total Number of Verbs'] = df.loc[value + 1:, 'Number of Verbs'].sum()
#         df_ch.at[i, 'Average Number of Verbs'] = df.loc[value + 1:, 'Number of Verbs'].mean()
#         df_ch.at[i, 'Total Number of Adjectives'] = df.loc[value + 1:, 'Number of Adjectives'].sum()
#         df_ch.at[i, 'Average Number of Adjectives'] = df.loc[value + 1:, 'Number of Adjectives'].mean()
#
# # Expanding mean takes into account all previous values, rolling mean only takes into account a window of values
# df_ch['Number of Sentences Expanding Mean'] = df_ch[
#     'Number of Sentences'].expanding().mean()  # .rolling(window=2).mean()
# df_ch['Average Polarity Expanding Mean'] = df_ch['Average Polarity'].expanding().mean()
# df_ch['Average Subjectivity Expanding Mean'] = df_ch['Average Subjectivity'].expanding().mean()
# df_ch['Total Number of Words Expanding Mean'] = df_ch['Total Number of Words'].expanding().mean()
# df_ch['Total Number of Nouns Expanding Mean'] = df_ch['Total Number of Nouns'].expanding().mean()
# df_ch['Total Number of Verbs Expanding Mean'] = df_ch['Total Number of Verbs'].expanding().mean()
# df_ch['Total Number of Adjectives Expanding Mean'] = df_ch['Total Number of Adjectives'].expanding().mean()
# df_ch['Average Number of Words Expanding Mean'] = df_ch['Average Number of Words'].expanding().mean()
# df_ch['Average Number of Nouns Expanding Mean'] = df_ch['Average Number of Nouns'].expanding().mean()
# df_ch['Average Number of Verbs Expanding Mean'] = df_ch['Average Number of Verbs'].expanding().mean()
# df_ch['Average Number of Adjectives Expanding Mean'] = df_ch['Average Number of Adjectives'].expanding().mean()
#
# # Saves chapter dataframe to csv
# df_ch.to_csv('Chapters.csv')
# print(df_ch.head())
#
# # Plots for Chapter Data
# ax2 = df_ch.plot.line(x=df_ch.index, y=['Average Polarity Expanding Mean', 'Average Subjectivity Expanding Mean'],
#                       marker='o', path_effects=[pe.Stroke(linewidth=3, foreground='k'), pe.Normal()])
# df_ch[['Average Polarity', 'Average Subjectivity']].plot(kind='bar',
#                                                          title='Average Polarity and Average Subjectivity per Chapter',
#                                                          figsize=(19.2, 10.8), legend=True, fontsize=12,
#                                                          xticks=df_ch.index, rot=90, ax=ax2)
# ax2.set_xlabel('Chapter')
# ax2.set_ylabel('Average Polarity and Average Subjectivity')
# ax2.set_xticklabels(df_ch['Chapter'])
# plt.savefig('Average Polarity and Average Subjectivity per Chapter.png', bbox_inches="tight")
#
# ax3 = df_ch.plot.line(x=df_ch.index, y='Number of Sentences Expanding Mean', marker='o',
#                       path_effects=[pe.Stroke(linewidth=3, foreground='k'), pe.Normal()])
# df_ch[['Number of Sentences']].plot(kind='bar', title='Number of Sentences per Chapter', figsize=(19.2, 10.8),
#                                     legend=True, fontsize=12, xticks=df_ch.index, rot=90, ax=ax3)
# ax3.set_xlabel('Chapter')
# ax3.set_ylabel('Number of Sentences')
# ax3.set_xticklabels(df_ch['Chapter'])
# plt.savefig('Number of Sentences per Chapter.png', bbox_inches="tight")
#
# ax4 = df_ch.plot.line(x=df_ch.index, y='Total Number of Words Expanding Mean', marker='o',
#                       path_effects=[pe.Stroke(linewidth=3, foreground='k'), pe.Normal()])
# df_ch[['Total Number of Words']].plot(kind='bar', title='Number of Words per Chapter', figsize=(19.2, 10.8),
#                                       legend=True, fontsize=12, xticks=df_ch.index, rot=90, ax=ax4)
# ax4.set_xlabel('Chapter')
# ax4.set_ylabel('Words')
# ax4.set_xticklabels(df_ch['Chapter'])
# plt.savefig('Number of Words per Chapter.png', bbox_inches="tight")
#
# ax5 = df_ch.plot.line(x=df_ch.index, y=['Total Number of Nouns Expanding Mean', 'Total Number of Verbs Expanding Mean',
#                                         'Total Number of Adjectives Expanding Mean'], marker='o',
#                       path_effects=[pe.Stroke(linewidth=3, foreground='k'), pe.Normal()])
# df_ch[['Total Number of Nouns', 'Total Number of Verbs', 'Total Number of Adjectives']].plot(kind='bar',
#                                                                                              title='Specific Number of Words per Chapter',
#                                                                                              figsize=(19.2, 10.8),
#                                                                                              legend=True, fontsize=12,
#                                                                                              xticks=df_ch.index, rot=90,
#                                                                                              ax=ax5)
# ax5.set_xlabel('Chapter')
# ax5.set_ylabel('Words')
# ax5.set_xticklabels(df_ch['Chapter'])
# plt.savefig('Specific Number of Words per Chapter.png', bbox_inches="tight")
#
# ax6 = df_ch.plot.line(x=df_ch.index, y='Average Number of Words Expanding Mean', marker='o',
#                       path_effects=[pe.Stroke(linewidth=3, foreground='k'), pe.Normal()])
# df_ch[['Average Number of Words']].plot(kind='bar', title='Average Number of Words per Chapter', figsize=(19.2, 10.8),
#                                         legend=True, fontsize=12, xticks=df_ch.index, rot=90, ax=ax6)
# ax6.set_xlabel('Chapter')
# ax6.set_ylabel('Average Words')
# ax6.set_xticklabels(df_ch['Chapter'])
# plt.savefig('Average Number of Words per Chapter.png', bbox_inches="tight")
#
# ax7 = df_ch.plot.line(x=df_ch.index,
#                       y=['Average Number of Nouns Expanding Mean', 'Average Number of Verbs Expanding Mean',
#                          'Average Number of Adjectives Expanding Mean'], marker='o',
#                       path_effects=[pe.Stroke(linewidth=3, foreground='k'), pe.Normal()])
# df_ch[['Average Number of Nouns', 'Average Number of Verbs', 'Average Number of Adjectives']].plot(kind='bar',
#                                                                                                    title='Specific Average Number of Words per Chapter',
#                                                                                                    figsize=(19.2, 10.8),
#                                                                                                    legend=True,
#                                                                                                    fontsize=12,
#                                                                                                    xticks=df_ch.index,
#                                                                                                    rot=90, ax=ax7)
# ax7.set_xlabel('Chapter')
# ax7.set_ylabel('Average Words')
# ax7.set_xticklabels(df_ch['Chapter'])
# plt.savefig('Average Specific Number of Words per Chapter.png', bbox_inches="tight")
#
# fig2, (ax8, ax9) = plt.subplots(2, 1, figsize=(19.2, 10.8))
# fig2.subplots_adjust(hspace=.5)
#
# h = sorted(df_ch['Total Number of Words'])
# ax8.hist(h, bins='auto', color='tab:blue')
# ax8.set_title(
#     'Total Number of Words per Chapter $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax8.set_ylabel('Number of Occurrences', color='tab:blue')
# ax8.tick_params('y', color='tab:blue')
#
# h = sorted(df_ch['Average Number of Words'])
# ax9.hist(h, bins='auto', color='tab:blue')
# ax9.set_title(
#     'Avg. Number of Words per Chapter $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax9.set_ylabel('Number of Occurrences', color='tab:blue')
# ax9.tick_params('y', color='tab:blue')
#
# fig2.savefig('Histogram of Words per Chapter.png', bbox_inches="tight")
#
# fig3, (ax10, ax11) = plt.subplots(2, 1, figsize=(19.2, 10.8))
# fig3.subplots_adjust(hspace=.5)
# h = sorted(df_ch['Average Polarity'])
# ax10.hist(h, bins='auto', color='tab:blue')
# ax10.set_title('Avg. Polarity per Chapter $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax10.set_ylabel('Number of Occurrences', color='tab:blue')
# ax10.tick_params('y', color='tab:blue')
#
# h = sorted(df_ch['Average Subjectivity'])
# ax11.hist(h, bins='auto', color='tab:blue')
# ax11.set_title(
#     'Avg. Subjectivity per Chapter $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax11.set_ylabel('Number of Occurrences', color='tab:blue')
# ax11.tick_params('y', color='tab:blue')
#
# fig3.savefig('Histogram of Polarity and Subjectivity per Chapter.png', bbox_inches="tight")
#
# fig4, [(ax12, ax13), (ax14, ax15), (ax16, ax17)] = plt.subplots(3, 2, figsize=(19.2, 10.8))
# fig4.subplots_adjust(hspace=.5)
#
# h = sorted(df_ch['Total Number of Nouns'])
# ax12.hist(h, bins='auto', color='tab:blue')
# ax12.set_title(
#     'Total Number of Nouns per Chapter $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax12.set_ylabel('Number of Occurrences', color='tab:blue')
# ax12.tick_params('y', color='tab:blue')
#
# h = sorted(df_ch['Average Number of Nouns'])
# ax13.hist(h, bins='auto', color='tab:blue')
# ax13.set_title(
#     'Avg. Number of Nouns per Chapter $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax13.set_ylabel('Number of Occurrences', color='tab:blue')
# ax13.tick_params('y', color='tab:blue')
#
# h = sorted(df_ch['Total Number of Verbs'])
# ax14.hist(h, bins='auto', color='tab:blue')
# ax14.set_title(
#     'Total Number of Verbs per Chapter $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax14.set_ylabel('Number of Occurrences', color='tab:blue')
# ax14.tick_params('y', color='tab:blue')
#
# h = sorted(df_ch['Average Number of Verbs'])
# ax15.hist(h, bins='auto', color='tab:blue')
# ax15.set_title(
#     'Avg. Number of Verbs per Chapter $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax15.set_ylabel('Number of Occurrences', color='tab:blue')
# ax15.tick_params('y', color='tab:blue')
#
# h = sorted(df_ch['Total Number of Adjectives'])
# ax16.hist(h, bins='auto', color='tab:blue')
# ax16.set_title('Total Number of Adjectives per Chapter $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(
#     round(np.std(h), 4)))
# ax16.set_ylabel('Number of Occurrences', color='tab:blue')
# ax16.tick_params('y', color='tab:blue')
#
# h = sorted(df_ch['Average Number of Adjectives'])
# ax17.hist(h, bins='auto', color='tab:blue')
# ax17.set_title(
#     'Number of Adjectives per Chapter $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax17.set_ylabel('Number of Occurrences', color='tab:blue')
# ax17.tick_params('y', color='tab:blue')
#
# fig4.savefig('Histogram of Specific Words per Chapter.png', bbox_inches="tight")
#
# fig6, ax24 = plt.subplots(figsize=(19.2, 10.8))
# fig6.subplots_adjust(hspace=.5)
#
# h = sorted(df_ch['Number of Sentences'])
# ax24.hist(h, bins='auto', color='tab:blue')
# ax24.set_title(
#     'Number of Sentences per Chapter $\mu=$' + str(round(np.mean(h), 4)) + ' $\sigma=$' + str(round(np.std(h), 4)))
# ax24.set_ylabel('Number of Occurrences', color='tab:blue')
# ax24.tick_params('y', color='tab:blue')
#
# fig6.savefig('Histogram of Number of Sentences per Chapter.png', bbox_inches="tight")
#
# df_ch = df_ch.apply(pd.to_numeric, errors='ignore')  # Converts suitable columns to numeric (some are object)
#
# print('Mean Number of Sentences per Chapter: ', df_ch['Number of Sentences'].mean())
# print('Mean Total Number of Words per Chapter: ', df_ch['Total Number of Words'].mean())
# print('Mean Average Number of Words per Chapter: ', df_ch['Average Number of Words'].mean())
# print('Mean Average Polarity per Chapter: ', df_ch['Average Polarity'].mean())
# print('Mean Average Subjectivity per Chapter: ', df_ch['Average Subjectivity'].mean())
# print('Mean Total Number of Nouns per Chapter: ', df_ch['Total Number of Nouns'].mean())
# print('Mean Average Number of Nouns per Chapter: ', df_ch['Average Number of Nouns'].mean())
# print('Mean Total Number of Verbs per Chapter: ', df_ch['Total Number of Verbs'].mean())
# print('Mean Average Number of Verbs per Chapter: ', df_ch['Average Number of Verbs'].mean())
# print('Mean Total Number of Adjectives per Chapter: ', df_ch['Total Number of Adjectives'].mean())
# print('Mean Average Number of Adjectives per Chapter: ', df_ch['Average Number of Adjectives'].mean())
#
# # Calculates the Top 3 and Bottom 3 values of data and outputs them into HTML format for website
# print('Chapters with Most Number of Sentences: \n',
#       df_ch.nlargest(3, 'Number of Sentences')[['Chapter', 'Number of Sentences']].to_html(index=False))
# print('Chapters with Least Number of Sentences: \n',
#       df_ch.nsmallest(3, 'Number of Sentences')[['Chapter', 'Number of Sentences']].to_html(index=False))
#
# print('Chapters with Most Total Number of Words: \n',
#       df_ch.nlargest(3, 'Total Number of Words')[['Chapter', 'Total Number of Words']].to_html(index=False))
# print('Chapters with Least Total Number of Words: \n',
#       df_ch.nsmallest(3, 'Total Number of Words')[['Chapter', 'Total Number of Words']].to_html(index=False))
#
# print('Chapters with Most Average Number of Words: \n',
#       df_ch.nlargest(3, 'Average Number of Words')[['Chapter', 'Average Number of Words']].to_html(index=False))
# print('Chapters with Least Average Number of Words: \n',
#       df_ch.nsmallest(3, 'Average Number of Words')[['Chapter', 'Average Number of Words']].to_html(index=False))
#
# print('Chapters with Most Average Polarity: \n',
#       df_ch.nlargest(3, 'Average Polarity')[['Chapter', 'Average Polarity']].to_html(index=False))
# print('Chapters with Least Average Polarity: \n',
#       df_ch.nsmallest(3, 'Average Polarity')[['Chapter', 'Average Polarity']].to_html(index=False))
#
# print('Chapters with Most Average Subjectivity: \n',
#       df_ch.nlargest(3, 'Average Subjectivity')[['Chapter', 'Average Subjectivity']].to_html(index=False))
# print('Chapters with Least Average Subjectivity: \n',
#       df_ch.nsmallest(3, 'Average Subjectivity')[['Chapter', 'Average Subjectivity']].to_html(index=False))
#
# print('Chapters with Most Total Number of Nouns: \n',
#       df_ch.nlargest(3, 'Total Number of Nouns')[['Chapter', 'Total Number of Nouns']].to_html(index=False))
# print('Chapters with Least Total Number of Nouns: \n',
#       df_ch.nsmallest(3, 'Total Number of Nouns')[['Chapter', 'Total Number of Nouns']].to_html(index=False))
#
# print('Chapters with Most Average Number of Nouns: \n',
#       df_ch.nlargest(3, 'Average Number of Nouns')[['Chapter', 'Average Number of Nouns']].to_html(index=False))
# print('Chapters with Least Average Number of Nouns: \n',
#       df_ch.nsmallest(3, 'Average Number of Nouns')[['Chapter', 'Average Number of Nouns']].to_html(index=False))
#
# print('Chapters with Most Total Number of Verbs: \n',
#       df_ch.nlargest(3, 'Total Number of Verbs')[['Chapter', 'Total Number of Verbs']].to_html(index=False))
# print('Chapters with Least Total Number of Verbs: \n',
#       df_ch.nsmallest(3, 'Total Number of Verbs')[['Chapter', 'Total Number of Verbs']].to_html(index=False))
#
# print('Chapters with Most Average Number of Verbs: \n',
#       df_ch.nlargest(3, 'Average Number of Verbs')[['Chapter', 'Average Number of Verbs']].to_html(index=False))
# print('Chapters with Least Average Number of Verbs: \n',
#       df_ch.nsmallest(3, 'Average Number of Verbs')[['Chapter', 'Average Number of Verbs']].to_html(index=False))
#
# print('Chapters with Most Total Number of Adjectives: \n',
#       df_ch.nlargest(3, 'Total Number of Adjectives')[['Chapter', 'Total Number of Adjectives']].to_html(index=False))
# print('Chapters with Least Total Number of Adjectives: \n',
#       df_ch.nsmallest(3, 'Total Number of Adjectives')[['Chapter', 'Total Number of Adjectives']].to_html(index=False))
#
# print('Chapters with Most Average Number of Adjectives: \n',
#       df_ch.nlargest(3, 'Average Number of Adjectives')[['Chapter', 'Average Number of Adjectives']].to_html(
#           index=False))
# print('Chapters with Least Average Number of Adjectives: \n',
#       df_ch.nsmallest(3, 'Average Number of Adjectives')[['Chapter', 'Average Number of Adjectives']].to_html(
#           index=False))
#
# plt.show()