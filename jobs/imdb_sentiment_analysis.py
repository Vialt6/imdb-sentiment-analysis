from io import BytesIO
import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt
from pyspark.sql.functions import StringType
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import base64
import dash_bootstrap_components as dbc
#from dash_bootstrap_components import BOOTSTRAP



spark = SparkSession.builder \
      .master("local[2]") \
      .appName("SparkByExamples.com") \
      .getOrCreate()

#Reading dataset
movie_df = pd.read_csv('../IMDB Dataset.csv')
classNameContent = StructType([StructField("review", StringType(), True),
                               StructField("sentiment",  StringType(), True)])
df = spark.createDataFrame(movie_df, classNameContent)
df.createTempView("MovieReviews")


#Read the clean df
clean_df = spark.read.parquet("../tmp/clean_df")
#clean_df.show()



#Word count

#Common words in text
#applying split funcion and explode to extract words from each column to see the Top words
top_20_words = spark.read.parquet("../tmp/top_20_words")


#Top 20 bigram: a pair of consecutive written units such as letters, syllables, or words.
#using the pyspark.ml library "ngram" for feature extraction
top_20_bigrams = spark.read.parquet("../tmp/top_20_bigrams")

#Top 20 trigram: a group of three consecutive written units such as letters, syllables, or words.
#Same as top 20 bigram
top_20_trigrams = spark.read.parquet("../tmp/top_20_trigrams")

#Only positive and onnly negative
only_positive_df = spark.read.parquet("../tmp/only_positive")
only_negative_df = spark.read.parquet("../tmp/only_negative")

#number of words and characters in positive reviews
num_of_wordP = spark.read.parquet("../tmp/num_words_positive")
num_of_charsP = spark.read.parquet("../tmp/num_chars_positive")
#num_of_wordP.sort(f.desc("wordCount")).show(20)


#number of words and characters in negative reviews
num_of_wordN = spark.read.parquet("../tmp/num_words_negative")
num_of_charsN = spark.read.parquet("../tmp/num_chars_negative")
#num_of_wordN.sort(f.desc("wordCount")).show(20)

#sentiment score neg neu pos
sentiment_score = spark.read.parquet("../tmp/sentiment_score")

#top 20 positive review
top_20_pos_review = spark.read.parquet("../tmp/top_20_pos_review")

#top 20 negative review
top_20_neg_review = spark.read.parquet("../tmp/top_20_neg_review")

#top 20 words in positive review
top_20_words_positive = spark.read.parquet("../tmp/top_20_words_positive")

#top 20 words in negative review
top_20_words_negative = spark.read.parquet("../tmp/top_20_words_negative")

#Df Director
director_df = spark.read.parquet("../tmp/director_df")

#top 10 film based on positive and negative score
top_10_pos_film = spark.read.parquet("../tmp/top_10_pos_film")
top_10_neg_film = spark.read.parquet("../tmp/top_10_neg_film")

#Rating df
rating_df = spark.read.parquet("../tmp/rating_df")

#compound rating
compound_rating = spark.read.parquet("../tmp/compound_rating_df")

#model Result df
result_df = spark.read.parquet("../tmp/result_model_df")




#Convert the "spark df" to a pandas df
pdf1 = df.toPandas()
clean_df_pandas=clean_df.toPandas()
only_positive_pandas = only_positive_df.toPandas()
only_negative_pandas = only_negative_df.toPandas()
top_20_words_pandas = top_20_words.toPandas()
top_20_bigrams_pandas=top_20_bigrams.toPandas()
top_20_trigrams_pandas=top_20_trigrams.toPandas()
word_countPositive_pd = num_of_wordP.toPandas()
word_countNegative_pd = num_of_wordN.toPandas()
chars_countPositive_pd = num_of_charsP.toPandas()
chars_countNegative_pd = num_of_charsN.toPandas()
sentiment_score_pd = sentiment_score.toPandas()
top_20_pos_review_pandas = top_20_pos_review.toPandas()
top_20_neg_review_pandas = top_20_neg_review.toPandas()
top_20_words_positive_pandas = top_20_words_positive.toPandas()
top_20_words_negative_pandas = top_20_words_negative.toPandas()
director_df_pandas = director_df.toPandas()
top_10_pos_film_pandas = top_10_pos_film.toPandas()
top_10_neg_film_pandas = top_10_neg_film.toPandas()
rating_df_pandas = rating_df.toPandas()
result_df_pandas = result_df.toPandas()
compound_rating_pandas = compound_rating.toPandas()


top_20_pos_review_pandas['id'] = top_20_pos_review_pandas['id'].astype(str)
top_20_neg_review_pandas['id'] = top_20_neg_review_pandas['id'].astype(str)



#Dash app
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.MINTY])
app.title = "IMDB sentiment analysis"

#Figure section

#First histogram
fig = px.histogram(
    pdf1,
    title='Reviews based on "positive" or "negative" sentiment',
    x="sentiment",
    width=700, height=700,
    color_discrete_sequence = px.colors.qualitative.Pastel,

)


#Barplot top 20 words
fig_top_20_words = px.bar(
    top_20_words_pandas,
    x="count",
    y="word",
    title='Top 20 words in Text',
    orientation='h',
    width=700, height=700,
    color='word',
    color_discrete_sequence = px.colors.qualitative.Dark24,

)


#Barpolot top 20 bigrams
fig_top_20_bigrams = px.bar(
    top_20_bigrams_pandas,
    x="count",
    y="bigram",
    title='Top 20 bigrams in Text',
    orientation='h',
    width=700, height=700,
    color='bigram'
)


#Barplot top 20 trigrams
fig_top_20_trigrams = px.bar(
    top_20_trigrams_pandas,
    x="count",
    y="trigram",
    title='Top 20 trigrams in Text',
    orientation='h',
    width=700, height=700,
    color='trigram',
    color_discrete_sequence=px.colors.qualitative.Vivid
)

#Hist positive reviews
fig_count_positive = px.histogram(
    word_countPositive_pd,
    title='Number of words in positive reviews',
    x="wordCount",
    width=700, height=700,
    color_discrete_sequence= ['yellowgreen']
)


#Hist negative reviews
fig_count_negative = px.histogram(
    word_countNegative_pd,
    title='Number of words in negative reviews',
    x="wordCount",
    width=700, height=700,
    color_discrete_sequence= ['indianred']
)

#Hist positive char
fig_chararcter_positive = px.histogram(
    chars_countPositive_pd,
    title='Number of characters in positive reviews',
    x="number_of_character",
    width=700, height=700,
    color_discrete_sequence= ['yellowgreen']
)

#Hist negative char
fig_chararcter_negative = px.histogram(
    chars_countNegative_pd,
    title='Number of characters in negative reviews',
    x="number_of_character",
    width=700, height=700,
    color_discrete_sequence= ['indianred']
)

#Hist positive score
fig_sentiment_score_pos = px.histogram(
    sentiment_score_pd[sentiment_score_pd['pos']>0],
    title='Distribution of positive score',
    x='pos',
    width=700, height=700,
    color_discrete_sequence= ['lightskyblue']
)

#Hist negative score
fig_sentiment_score_neg = px.histogram(
    sentiment_score_pd[sentiment_score_pd['neg']>0],
    title='Distribution of negative score',
    x='neg',
    width=700, height=700,
    color_discrete_sequence= ['mediumorchid']
)

#Barplot top 20 words
fig_top_20_pos_review = px.bar(
    top_20_pos_review_pandas,
    x="pos",
    y="id",
    title='Top 20 positive reviews in Text',
    orientation='h',
    width=700, height=700,
    color='id',
    color_discrete_sequence=px.colors.qualitative.Light24
)

#Barplot top 20 negative review
fig_top_20_neg_review = px.bar(
    top_20_neg_review_pandas,
    x="neg",
    y="id",
    title='Top 20 negative reviews in Text',
    orientation='h',
    width=700, height=700,
    color='id',
    color_discrete_sequence=px.colors.qualitative.Dark24
)

#Barplot top 20 words in positive reviews
fig_top_20_words_positive = px.bar(
    top_20_words_positive_pandas,
    x="count",
    y="word",
    title='Top 20 words in positive reviews',
    orientation='h',
    width=700, height=700,
    color='word'
)

#Barplot top 20 words in negative reviews
fig_top_20_words_negative = px.bar(
    top_20_words_negative_pandas,
    x="count",
    y="word",
    title='Top 20 words in negative reviews',
    orientation='h',
    width=700, height=700,
    color='word'
)

#Treemap of top 20 words in positive reviews
figTree_top_20_words_positive = px.treemap(top_20_words_positive_pandas,
                                           path=['word'],
                                           values='count',
                                           title='Top 20 words in positive reviews')


#Treemap of top 20 words in negative reviews
figTree_top_20_words_negative = px.treemap(top_20_words_negative_pandas,
                                           path=['word'],
                                           values='count',
                                           title='Top 20 words in negative reviews')

#Barplot top 10 film based on positive score
fig_top_10_pos_film = px.bar(
    top_10_pos_film_pandas,
    x="title",
    y="compound",
    title='Top 10 positive film',
    #orientation='h',
    width=800, height=800,
    color='title',
    color_discrete_sequence=px.colors.qualitative.Light24
)

#Barplot top 10  film based on negative score
fig_top_10_neg_film = px.bar(
    top_10_neg_film_pandas,
    x="title",
    y="compound",
    title='Top 10 negative film',
    #orientation='h',
    width=700, height=700,
    color='title',
    color_discrete_sequence=px.colors.qualitative.Dark24
)

#Hist rating df
rating_distribution = px.histogram(
    rating_df_pandas,
    title='Distribution of rating in the reviews',
    x="rating",
    width=700, height=700
).update_xaxes(categoryorder='total ascending')

#Hist negative score
fig_compound_dist = px.histogram(
    sentiment_score_pd['compound'],
    title='Distribution of compound score',
    x='compound',
    width=700, height=700,
    color_discrete_sequence= ['mediumorchid']
)




#Barplot Accuracy
fig_accuracy = px.bar(
    result_df_pandas,
    x="classifier",
    y="accuracy",
    title='Accuracy score',
    width=700, height=700,
    color='classifier'
)

#Barplot F1
fig_f1 = px.bar(
    result_df_pandas,
    x="classifier",
    y="f1",
    title='F1 score',
    width=700, height=700,
    color='classifier'
)

#Barplot precision
fig_precision = px.bar(
    result_df_pandas,
    x="classifier",
    y="precision",
    title='Precision score',
    width=700, height=700,
    color='classifier'
)

#Barplot recall
fig_recall = px.bar(
    result_df_pandas,
    x="classifier",
    y="recall",
    title='Recall score',
    width=700, height=700,
    color='classifier'
)




#Making wordcloud for positive and negative
def plot_wordcloud(df,title,column):
    plt.figure(figsize = (20,20))
    wc = WordCloud(max_words = 500 , width = 800 , height = 300).generate(" ".join(df.review))
    plt.title(title, fontsize=13)
    return wc.to_image()

#Making wordcloud for directors
def plot_wordcloud_director(df,title,column):
    plt.figure(figsize = (20,20))
    wc = WordCloud(max_words = 100 , width = 800 , height = 300).generate(" ".join(df.director))
    plt.title(title, fontsize=13)
    return wc.to_image()

#need to convert to an img
@app.callback(dash.dependencies.Output('image_wc_positive', 'src'), [dash.dependencies.Input('image_wc_positive','id')])
def make_image_positive_wc(b):
    img=BytesIO()
    plot_wordcloud(df=only_positive_pandas,title="Positive Wordcloud",column="positive").save(img,format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

@app.callback(dash.dependencies.Output('image_wc_negative', 'src'), [dash.dependencies.Input('image_wc_negative','id')])
def make_image_negative_wc(b):
    img=BytesIO()
    plot_wordcloud(df=only_negative_pandas,title="Negative Wordcloud",column="negative").save(img,format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

@app.callback(dash.dependencies.Output('image_wc_director', 'src'), [dash.dependencies.Input('image_wc_director','id')])
def make_image_director_wc(b):
    img=BytesIO()
    plot_wordcloud_director(df=director_df_pandas,title="Director Wordcloud",column="director").save(img,format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

#Top 20 words/bigrams/trigrams
@app.callback(dash.dependencies.Output('graph_ngrams', 'figure'),
              [dash.dependencies.Input(component_id='dropdown_ngrams', component_property='value')]
              )
def n_grams_image(value):
    if value == 'top_20_words':
        fig = fig_top_20_words
        return fig
    if value == 'top_20_bigrams':
        fig = fig_top_20_bigrams
        return fig
    if value == 'top_20_trigrams':
        fig = fig_top_20_trigrams
        return fig

#Word count pos/neg
@app.callback(Output('graph_word_count','figure'), [Input(component_id='dropdown_wc',component_property='value')])
def word_count_image(value):
    if value == 'wc_pos':
        fig = fig_count_positive
        return fig
    if value == 'wc_neg':
        fig = fig_count_negative
        return fig

#Char count pos/neg
@app.callback(Output('graph_char_count','figure'), [Input(component_id='dropdown_char_count',component_property='value')])
def word_count_image(value):
    if value == 'char_count_pos':
        fig = fig_chararcter_positive
        return fig
    if value == 'char_count_neg':
        fig = fig_chararcter_negative
        return fig

#Top 20 pos/neg reviews
@app.callback(Output('graph_top_20_review_pos_neg','figure'), [Input(component_id='dropdown_top_20_review_pos_neg',component_property='value')])
def top_20_pos_neg_review_image(value):
    if value == 'top_20_pos_review':
        fig = fig_top_20_pos_review
        return fig
    if value == 'top_20_neg_review':
        fig = fig_top_20_neg_review
        return fig

#Sentiment score pos/neg
@app.callback(Output('graph_sentiment_score','figure'), [Input(component_id='dropdown_sentiment_score',component_property='value')])
def sentiment_score_fig(value):
    if value == 'sentiment_pos':
        fig = fig_sentiment_score_pos
        return fig
    if value == 'sentiment_neg':
        fig = fig_sentiment_score_neg
        return fig

#Taking besst and worst review
the_best_review = top_20_pos_review_pandas['review'].iloc[0]
the_worst_review = top_20_neg_review_pandas['review'].iloc[0]


#top 20 words based on score
@app.callback(Output('graph_top_20_words_review_pos_neg','figure'), [Input(component_id='dropdown_top_20_words_review_pos_neg',component_property='value')])
def top_20_words_pos_neg_review_image(value):
    if value == 'top_20_words_pos_review':
        fig = fig_top_20_words_positive
        return fig
    if value == 'top_20_words_neg_review':
        fig = fig_top_20_words_negative
        return fig

#graph for top 10 film based on negative and positive score
@app.callback(Output('graph_top_10_film_pos_neg_score','figure'), [Input(component_id='dropdown_top_10_film_pos_neg_score',component_property='value')])
def top_10_film_pos_neg_score_image(value):
    if value == 'top_10_pos_film':
        fig = fig_top_10_pos_film
        return fig
    if value == 'top_10_neg_film':
        fig = fig_top_10_neg_film
        return fig



avg_pos_word = round(word_countPositive_pd["wordCount"].mean(),2)
avg_neg_word = round(word_countNegative_pd["wordCount"].mean(),2)
avg_num_char_pos = round(chars_countPositive_pd["number_of_character"].mean(),2)
avg_num_char_neg = round(chars_countNegative_pd["number_of_character"].mean(),2)
avg_pos_score = round(sentiment_score_pd["pos"].mean(),2)
avg_neg_score = round(sentiment_score_pd["neg"].mean(),2)
rating_df_pandas['rating'] = rating_df_pandas['rating'].astype(int)
avg_rating = round(rating_df_pandas["rating"].mean(), 2)



# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


sidebar = html.Div(
    [
        dbc.Col([
                dbc.Card([
                        dbc.CardImg(
                            src="https://1000logos.net/wp-content/uploads/2020/08/Imdb-Logo-2016.png",
                            bottom=True),
                ],
            style={"width": "10rem"},
            )
            ],

            width={"offset": 2}

        ),


        #html.H2("IMDB", className="display-4"),
        html.Hr(),
        html.P(
            "Browse through the different sections to see what's there", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
                dbc.NavLink("Page 3", href="/page-3", active="exact"),
                dbc.NavLink("Page 4", href="/page-4", active="exact"),
                dbc.NavLink("Prediction Results", href="/prediction", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

home = html.Div(
        children=[
            html.P(children="🎥🍿🎬📺", className="header-emoji", style={'textAlign':'center'}),
            html.H1(
                children="IMDb sentiment analysis", className="header-title",
                style={
                    'textAlign': 'center',
                    'color': 'black',
                    'font-family': 'impact',

                }
            ),
            html.Br(),
            html.P(
                children=""
                         "This is a dashboard for the Big Data Project using Pyspark and Dash."
                         " The project involves analyzing reviews from the IMDB website and classifying them as either "
                         "positive or negative based on the sentiment column in the dataset."
                         " The dataset consists of two columns: \"review\" and \"sentiment\","
                         " where the review column contains the text of the review and the sentiment column "
                         "indicates whether the review is positive or negative.",
                className="header-description",
                style={
                    'textAlign': 'center',
                    'color':'black',
                    'font-size' : '18px'
                }
            ),

            html.Br(),

            #image of films
            dbc.Col([
                dbc.Card([
                        dbc.CardImg(
                            src="https://external-preview.redd.it/Z-mdOCdgw53wluJKQdklW2-WwJEcd3zXoER3YNl-euI.jpg?auto=webp&s=9da2a0406734c547c7bc489c5fa20b091c7ee86c",
                            bottom=True),
                ],
            style={"width": "70rem"},
            )
            ]),






            ],
)


page1 = html.Div(
        children=[
            html.P(children="🎥🍿🎬📺", className="header-emoji", style={'textAlign':'center'}),
            html.H1(
                children="IMDb sentiment analysis", className="header-title",
                style={
                    'textAlign': 'center',
                    'color': 'black',
                    'font-family': 'impact'

                }
            ),

            html.Div(children=[
                html.Div([
                    dcc.Graph(id="sentiment", figure=fig),
                ], style={'display':'inline-block'}),
                html.Div([
                    html.Label(['Chose a graph:']),
                    dcc.Dropdown(
                    id='dropdown_ngrams',
                    options=[
                        {'label': 'Top 20 words', 'value': 'top_20_words'},
                        {'label': 'Top 20 bigrams', 'value': 'top_20_bigrams'},
                        {'label': 'Top 20 trigrams', 'value': 'top_20_trigrams'},
                    ],
                    value='top_20_words',
                ),
                html.Div(dcc.Graph(id='graph_ngrams'))
                ],style={'display':'inline-block'}),
                html.P("Word Cloud for positive reviews",
                       style={'color': 'black',
                              'font-size' : '18px'}
                       ),
                html.Img(id="image_wc_positive"),
                html.P(),
                html.Div(),
                html.P(""
                       "Word Cloud for negative reviews",
                       style={'color': 'black',
                              'font-size' : '18px'}
                       ),
                html.Img(id="image_wc_negative"),

            ], style={'width': '30%', 'display': 'inline-block'}),
        ])



page2 = html.Div(
        children=[
            html.P(children="🎥🍿🎬📺", className="header-emoji", style={'textAlign':'center'}),
            html.H1(
                children="IMDb sentiment analysis", className="header-title",
                style={
                    'textAlign': 'center',
                    'color': 'black',
                    'font-family': 'impact'

                }
            ),
            html.Div(children=[
                html.Div([
                    html.Label(['Chose a graph:']),
                    dcc.Dropdown(
                    id='dropdown_wc',
                    options=[
                        {'label': 'Word count positive review', 'value': 'wc_pos'},
                        {'label': 'Word count negative review', 'value': 'wc_neg'},
                    ],
                    value='wc_pos',
                ),
                dbc.Col(dcc.Graph(id='graph_word_count',style={'display': 'flexible'}), width=3),
                html.P('Average positive word length:',
                       style={'color': 'black'}
                       ),
                html.P(avg_pos_word,
                       style={'color': 'yellowgreen'}),
                html.P('Average negative word length:',
                       style={'color': 'black'}),
                html.P(avg_neg_word,
                       style={'color': 'indianred'}),

                ],style={'display':'flexible'}),

            ], style={'width': '30%', 'display': 'flexible'}),
            html.Div(children=[
                html.Div([
                    html.Label(['Chose a graph:']),
                    dcc.Dropdown(
                        id='dropdown_char_count',
                        options=[
                            {'label': 'Number of character in positive review', 'value': 'char_count_pos'},
                            {'label': 'Number of character in negative review', 'value': 'char_count_neg'},
                        ],
                        value='char_count_pos',
                    ),
                    dbc.Col(dcc.Graph(id='graph_char_count',style={'display': 'flexible'}), width=3),
                    html.P('Average number of characters in positive reviews:',
                           style={'color': 'black'}),
                    html.P(avg_num_char_pos,
                           style={'color': 'yellowgreen'}),
                    html.P('Average number of characters in negative reviews:',
                           style={'color': 'black'}),
                    html.P(avg_num_char_neg,
                           style={'color': 'indianred'}),
                ], style={'display': 'flexible'}),

            ], style={'width': '30%', 'display': 'flexible'}),
            html.Div(children=[
                html.Div([
                    html.Label(['Chose a graph:']),
                    dcc.Dropdown(
                        id='dropdown_top_20_words_review_pos_neg',
                        options=[
                            {'label': 'Top 20 words in positive reviews', 'value': 'top_20_words_pos_review'},
                            {'label': 'Top 20 words in negative reviews', 'value': 'top_20_words_neg_review'},
                        ],
                        value='top_20_words_pos_review',
                    ),
                    dbc.Col(dcc.Graph(id='graph_top_20_words_review_pos_neg',style={'display': 'flexible'}), width=3)
                ], style={'display': 'flexible'}),

            ], style={'width': '30%', 'display': 'flexible'}),


           html.Div([
                    dcc.Graph(id="top_20_words_pos", figure= figTree_top_20_words_positive),
                ], style={'display':'inline-block'}),

           html.Div([
                    dcc.Graph(id="top_20_words_neg", figure= figTree_top_20_words_negative),
                ], style={'display':'inline-block'}),

            ],

)

page3 = html.Div(
        children=[
            html.P(children="🎥🍿🎬📺", className="header-emoji", style={'textAlign':'center'}),
            html.H1(
                children="IMDb sentiment analysis", className="header-title",
                style={
                    'textAlign': 'center',
                    'color': 'black',
                    'font-family': 'impact'

                }
            ),
            html.Div(children=[
                html.Div([
                    html.Label(['Chose a graph:']),
                    dcc.Dropdown(
                    id='dropdown_top_20_review_pos_neg',
                    options=[
                        {'label': 'Top 20 positive reviews', 'value': 'top_20_pos_review'},
                        {'label': 'Top 20 negative reviews', 'value': 'top_20_neg_review'},
                    ],
                    value='top_20_pos_review',
                ),
                html.Div(dcc.Graph(id='graph_top_20_review_pos_neg')),
                ],style={'display':'inline-block'}),
                html.Div([
                    html.P("The Best review based on the positivity score is: ",
                           style={'color': 'black'}),
                    html.P(the_best_review,
                           style={'color': 'yellowgreen'}),
                    html.P("The Worst review based on the negativity score is: ",
                           style={'color': 'black'}),
                    html.P(the_worst_review,
                           style={'color': 'indianred'})
                ]),
                html.Div([
                    html.Label(['Chose a graph:']),
                    dcc.Dropdown(
                        id='dropdown_sentiment_score',
                        options=[
                            {'label': 'Positive score', 'value': 'sentiment_pos'},
                            {'label': 'Negative score', 'value': 'sentiment_neg'},
                        ],
                        value='sentiment_pos',
                    ),
                    html.Div(dcc.Graph(id='graph_sentiment_score')),
                    html.P("Average positivity score: ",
                           style={'color': 'black'}),
                    html.P(avg_pos_score,
                           style={'color': 'yellowgreen'}),
                    html.P("Average negativity score: ",
                           style={'color': 'black'}),
                    html.P(avg_neg_score,
                           style={'color': 'indianred'})
                ], style={'display': 'inline-block'}),
            ], style={'width': '30%', 'display': 'inline-block'}),







            ],
)

page4 = html.Div(
        children=[
            html.P(children="🎥🍿🎬📺", className="header-emoji", style={'textAlign':'center'}),
            html.H1(
                children="IMDb sentiment analysis", className="header-title",
                style={
                    'textAlign': 'center',
                    'color': 'black',
                    'font-family': 'impact'

                }
            ),
            html.Div(
            children=[
            html.Div(children=[
                html.Div([
                html.Label(['Chose a graph:']),
                dcc.Dropdown(
                    id='dropdown_top_10_film_pos_neg_score',
                    options=[
                        {'label': 'Top 10 positive films', 'value': 'top_10_pos_film'},
                        {'label': 'Top 10 negative films', 'value': 'top_10_neg_film'},
                    ],
                    value='top_10_pos_film',
                ),
                dbc.Col(dcc.Graph(id='graph_top_10_film_pos_neg_score', style={'display': 'flexible'}), width=3),
                html.Div(),
                html.P("Word Cloud for directors of films",
                       style={'color': 'black',
                              'font-size' : '18px'}),
                html.Img(id="image_wc_director"),
                html.Div(),
                dbc.Col(dcc.Graph(id='rating_distribution', figure=rating_distribution)),
                html.P("Average rating extracted from the reviews",
                       style={'color': 'black'}),
                html.P(avg_rating,
                       style={'color': 'black'}),

                html.Div(),
                dbc.Col(dcc.Graph(id='compound_distribution', figure=fig_compound_dist))
            ], style={'display': 'flexible'}),

        ], style={'width': '30%', 'display': 'flexible'}),
          ],)
        ],
)



prediction = html.Div(
        children=[
            html.P(children="🎥🍿🎬📺", className="header-emoji", style={'textAlign':'center'}),
            html.H1(
                children="IMDb sentiment analysis", className="header-title",
                style={
                    'textAlign': 'center',
                    'color': 'black',
                    'font-family': 'impact'

                }
            ),
            html.Div([
                html.Div(dcc.Graph(id='accuracy_score', figure=fig_accuracy)),
                html.Div(dcc.Graph(id='accuracy_score', figure=fig_f1)),
                html.Div(dcc.Graph(id='accuracy_score', figure=fig_precision)),
                html.Div(dcc.Graph(id='accuracy_score', figure=fig_recall)),
            ], style={'display': 'inline-block'}),




    ]

        )




content = html.Div(id="page-content", style=CONTENT_STYLE)


app.layout=html.Div(children = [
            html.Div([dcc.Location(id="url"), sidebar, content]),
        ],
        className="header"
    )
#Dash Layout section

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home
    elif pathname == "/page-1":
        return page1
    elif pathname == "/page-2":
        return page2
    elif pathname == "/page-3":
        return page3
    elif pathname == "/page-4":
        return page4
    elif pathname == "/prediction":
        return prediction
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )







if __name__ == "__main__":
    app.run_server(debug=True,dev_tools_ui=False)

