import emoji
import collections as c
import pandas as pd
import numpy as np
import streamlit as st
from matplotlib.lines import Line2D
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# for visualization
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import re
# word cloud
from wordcloud import WordCloud, STOPWORDS
import getpass



import numpy as np
import matplotlib.pyplot as plt



def authors_name(data):
    """
        It returns the name of participants in chat. 
    """
    authors = data.Author.unique().tolist()
    return [name for name in authors if name != None]


def extract_emojis(s):
    """
        This function is used to calculate emojis in text and return in a list.
    """

    return ''.join(c for c in s if c in emoji.UNICODE_EMOJI['en'])
    #return [c for c in s if c in emoji.UNICODE_EMOJI]


def stats(data):
    """
        This function takes input as data and return number of messages and total emojis used in chat.
    """
    total_messages = data.shape[0]
    media_messages = data[data['Message'] == '<Media omitted>'].shape[0]
    emojis = sum(data['emoji'].str.len())
    
    return " __Total Messages 💬:__ __{}__ \n\n __Total Media 🎬:__ __{}__ \n\n __Total Emoji's 😂:__ __{}__".format(total_messages, media_messages, emojis)


def popular_emoji(data):
    """
        This function returns the list of emoji's with it's frequency.
    """
    total_emojis_list = list([a for b in data.emoji for a in b])
    emoji_dict = dict(c.Counter(total_emojis_list))
    emoji_list = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
    return emoji_list


def visualize_emoji(data):
    """
        This function is used to make pie chart of popular emoji's.
    """
    emoji_df = pd.DataFrame(popular_emoji(data), columns=['emoji', 'count'])
    
    fig = px.pie(emoji_df, values='count', names='emoji')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    # fig.show()
    return fig

def word_cloud(df):
    """
        This function is used to generate word cloud using dataframe.
    """
    df = df[df['Message'] != '<Media omitted>']
    df = df[df['Message'] != 'This message was deleted']
    words = ' '.join(df['Message'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    # To stop article, punctuations
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    
    # plt.figure(figsize=(45,8))
    fig = plt.figure()
    ax = fig.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig
    

def active_date(data):
    """
        This function is used to generate horizontal bar graph between date and 
        number of messages dataframe.
    """
    fig, ax = plt.subplots()
    ax = data['Date'].value_counts().head(10).plot.barh()
    ax.set_title('Top 10 active date')
    ax.set_xlabel('Number of Messages')
    ax.set_ylabel('Date')
    plt.tight_layout()
    return fig
    
def active_time(data):
    """
    This function generate horizontal bar graph between time and number of messages.

    Parameters
    ----------
    data : Dataframe
        With this data graph is generated.

    Returns
    -------
    None.

    """
    fig, ax = plt.subplots()
    ax = data['Time'].value_counts().head(10).plot.barh()
    ax.set_title('Top 10 active time')
    ax.set_xlabel('Number of messages')
    ax.set_ylabel('Time')
    plt.tight_layout()
    return fig




def day_wise_count(data):
    """
    This function generate a line polar plot.

    Parameters
    ----------
    data : DataFrame
        DESCRIPTION.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    day_df = pd.DataFrame(data["Message"])
    day_df['day_of_date'] = data['Date'].dt.weekday
    day_df['day_of_date'] = day_df["day_of_date"].apply(lambda d: days[d])
    day_df["messagecount"] = 1
    
    day = day_df.groupby("day_of_date").sum()
    day.reset_index(inplace=True)
    
    fig = px.line_polar(day, r='messagecount', theta='day_of_date', line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
        )),
    showlegend=False
    )
    # fig.show()
    return fig


    import matplotlib
    matplotlib.rcParams['font.size'] = 20

    # Beautifying Default Styles using Seaborn
    sns.set_style("darkgrid")

    # Plotting;

    # PLOT 1: Messages grouped by weekday
    sns.barplot(grouped_by_day.day, grouped_by_day.message_count, order=days, ax = axs[0], palette='Pastel2_r')
    axs[0].set_title('Total messages sent grouped by day')

    # PLOT 2: Messages grouped by months
    sns.barplot(y = grouped_by_month.month, x=grouped_by_month.message_count, order = months, ax = axs[1], palette='Pastel1_d')
    axs[1].set_title('Total messages sent grouped by month');

    # Saving the plots;
    plt.savefig('days_and_month.svg', format = 'svg')


    return fig




def num_messages(data):
    """
    This function generates the line plot of number of messages on monthly basis.

    Parameters
    ----------
    data : DataFrame
        DESCRIPTION.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    data.loc[:, 'MessageCount'] = 1
    date_df = data.groupby("Date").sum()
    date_df.reset_index(inplace=True)
    fig = px.line(date_df, x="Date", y="MessageCount")
    fig.update_xaxes(nticks=20)
    # fig.show()
    return fig

def chatter(data):
    """
    This function generates a bar plot of members involve in a chat corressponding
    to the number of messages.

    Parameters
    ----------
    data : DataFrame
        DESCRIPTION.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    auth = data.groupby("Author").sum()
    auth.reset_index(inplace=True)
    fig = px.bar(auth, y="Author", x="MessageCount", color='Author', orientation="h",
             color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"],
             title='Number of messages corresponding to author'
            )
    # fig.show()
    return fig




def senti(data):
    df = pd.DataFrame(data, columns=["Date", 'Time', 'Author', 'Message'])
    df['Date'] = pd.to_datetime(df['Date'])

    data = df.dropna()
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sentiments = SentimentIntensityAnalyzer()
    data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["Message"]]
    data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["Message"]]
    data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["Message"]]
    #print(data.head())
    x = sum(data["Positive"])
    y = sum(data["Negative"])
    z = sum(data["Neutral"])

    def sentiment_score(a, b, c):
        if (a > b) and (a > c):
            print("Positive 😊 ")
        elif (b > a) and (b > c):
            print("Negative 😠 ")
        else:
            print("Neutral 🙂 ")

    sentiment_score(x, y, z)




#
# def network(data):
#     """Visualize response network structures.
#     Display how often users respond to each other user in an alluvial
#     diagram.
#     """
#     class LineDataUnits(Line2D):
#         """Line2D taking lw argument in y axis units instead of points"""
#         def __init__(self, *args, **kwargs):
#             _lw_data = kwargs.pop('lw', 1)
#             super().__init__(*args, **kwargs)
#             self._lw_data = _lw_data
#
#         def _get_lw(self):
#             if self.axes is not None:
#                 ppd = 72./self.axes.figure.dpi
#                 trans = self.axes.transData.transform
#                 return ((trans((1, self._lw_data)) - trans((0, 0))) * ppd)[1]
#             else:
#                 return 1
#
#         def _set_lw(self, lw):
#             self._lw_data = lw
#
#         _linewidth = property(_get_lw, _set_lw)
#
#     def ease(y0, y1):
#         """Return ease in out function from point (0, y0) to (1, y1)"""
#         return y0 + (y1-y0) * x**2 / (x**2 + (1-x)**2)
#
#     fig, ax = plt.subplots()
#     x = np.linspace(0.002, 0.998)
#     s = sum(Member.days) - 1
#     net = [[m.answers[c.name]/s if c.name in m.answers else 0 for c in data] for m in data]
#     spc = 0.05  # spacing between groups
#     posr = 1 + len(data)*spc
#     for i in range(len(data)):
#         for j, m in enumerate(data):
#             posl = 1 + (len(data)-1-j)*spc - sum([sum(net[k]) for k in range(j)])
#             posl -= sum(net[j][:i]) + net[j][i]
#             posr -= net[j][i] + (spc if j == 0 else 0)
#             # draw limitations
#             p = plt.bar(0, net[j][i], 0.002, posl, color='black', align='edge').patches[0]
#             plt.bar(1, net[j][i], -0.002, posr, color='black', align='edge')
#             # annotate segments with user names
#             if i == 0:
#                 tpos = 1 + len(data)*spc - spc
#                 tpos -= sum([sum(net[k]) for k in range(j)]) + sum(net[j])/2 + j*spc
#                 ax.text(-0.043, tpos, m.name, ha='right', va='center')
#             # draw alluvial lines
#             ax.add_line(LineDataUnits(
#                 x,
#                 ease(posl+net[j][i]/2, posr+net[j][i]/2),
#                 lw=net[j][i],
#                 alpha=0.6,
#                 color=COLORS[j+4]
#             ))
#
#     # set style attributes
#     plt.ylim(0, 1 + len(data)*spc - spc)
#     plt.title('Response Network')
#     ax.set_axis_off()

#
# def check():
#     # st.button("LOGIN")
#     database = {"Vanshika": "123456", "minor": "project"}
#
#     username = input("Enter Your Username : ")
#     password = getpass.getpass("Enter Your Password : ")
#     for i in database.keys():
#         if username == i:
#             while password != database.get(i):
#                 password = getpass.getpass("Enter Your Password Again : ")
#             break
#     print("Verified")
#     return login()
#
#     # return
