from datetime import datetime
from dateutil import parser
from ast import literal_eval

#querying
import pandas as pd
import numpy as np

#plotting
from plotly.offline import plot #to save graphs as html files, useful when testing
import plotly.graph_objs as go


#dashboarding
import dash
import dash_core_components as dcc
import dash_html_components as html


mapbox_access_token = 'pk.eyJ1Ijoiam9hb2ZvbnNlY2EiLCJhIjoiY2picXB3cDVvMDczYjJ3bzBxNDV3dGI0MSJ9.XpQDNjTuMAM-xckGln0KrA'


with open('support/active_keyword', 'r') as kw_filter:
    header_keyword=kw_filter.readline()

keyword = header_keyword.rstrip()
path = '../../Web_Crawler/_data/'
t = open(path + '%s_tweets.csv' % keyword, 'r')

tweets_df = pd.read_csv(t)

def drop_minutes_and_seconds(olddate):
    new_date = datetime.date(datetime(int(olddate.year), int(olddate.month), int(olddate.day), int(olddate.hour)))#.replace(minute=0, second=0, microsecond=0)
    return new_date

def filter_and_format_date(datestr):
    try:
        date = parser.parse(datestr)
    except (TypeError, ValueError) as e:
        date = 'none'
    return date

tweets_df['date'] = tweets_df['created_at'].apply(filter_and_format_date)
tweets_df_date = tweets_df[tweets_df.date != 'none']
tweets_df_date['date'].apply(drop_minutes_and_seconds)
tweets_df_date.sort_values(['date'], ascending=False)


#yvalues_ig_hist1 = tweets_df_date[['date']].groupby('date').size()
#
#xvalues = []
#for value in tweets_df['date']:
#    if value not in xvalues:
#        xvalues.append(value)
#yvalues = []
#for date in xvalues:
#    yvalues.append(yvalues_ig_hist1[date])


#plotting Ig posts
diff = (max(tweets_df_date['date'])-min(tweets_df_date['date']))
number_of_bins= (diff.days+1)*24
#first_ig_histogram = [go.Scatter(x=xvalues, y=yvalues)]
twt_histogram = [go.Histogram(x=tweets_df_date['date'], nbinsx=number_of_bins)]

hist_configuration= go.Layout(title='Tweets containing the keyword \'%s\'' % keyword, xaxis=dict(title='Hours'), yaxis=dict(title='Count'))
plot_twt_posts = go.Figure(data=twt_histogram, layout=hist_configuration)

flnm_posts_twt_histogram= 'support/' + keyword + '_posts_twt_histogram.html'
plot(plot_twt_posts, filename=flnm_posts_twt_histogram, show_link=False, auto_open=False)

t.close()

# =============================================================================
# plotting geomap
# =============================================================================

def convert_dicts(dict_string):
    if type(dict_string) is not float and dict_string[0] == '{':
        dict_string = literal_eval(dict_string)
    else:
        dict_string = np.NaN
    return dict_string

def get_lng(coordinates_dict):
    try:
        return coordinates_dict['coordinates'][0]
    except TypeError:
        return np.NaN

def get_lat(coordinates_dict):
    try:
        return coordinates_dict['coordinates'][1]
    except:
        return np.NaN


tweets_df['coordinates_wdicts']= tweets_df['coordinates'].apply(convert_dicts)
tweets_df['lat']=tweets_df['coordinates_wdicts'].apply(get_lat)
tweets_df['lng']=tweets_df['coordinates_wdicts'].apply(get_lng)


lon=[]
for coord in tweets_df['lng']:
    lon.append(coord)

lat=[]
for coord in tweets_df['lat']:
    lat.append(coord)

#size=

data = go.Data([
        go.Scattermapbox(
                lat=tweets_df['lat'],
                lon=tweets_df['lng'],
                mode='markers',
#                marker=go.Marker(
#                        size=[endpt_size] + [4 for j in range(len(steps) - 2)] + [endpt_size])
                text=tweets_df['text']
                )
        ])

layout = go.Layout(
    title='Location of Tweets',
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        style='dark',
        center=dict(
            lat=38.7,
            lon=-7.98,
        ),
        pitch=0,
        zoom=2.2
    ),
)
wonder_map = go.Figure(data=data, layout=layout)
plot(wonder_map, filename= 'support/' + keyword + '_scatterplottest.html', show_link=False, auto_open=False)

# =============================================================================
# last plot
# =============================================================================

#comments_data_datecount = tweets_df.groupby('date').agg({'comment_count': np.sum}).reset_index()
#tweets_df['postcount']=tweets_df['date']
#posts_data_datecount = tweets_df.groupby('date').agg({'postcount': np.count_nonzero}).reset_index()
#
#comments_plot= go.Bar(x=comments_data_datecount['date'], y=comments_data_datecount['comment_count'], name='Comments')
#posts_plot= go.Bar(x=posts_data_datecount['date'] ,y=posts_data_datecount['postcount'], name='Posts' )
#bar_chart_layout= go.Layout(title='Number of comments relative to posts', xaxis=dict(title='Days'), yaxis=dict(title='Count'))
#bar_chart_content = [posts_plot,comments_plot]
#last_bar_chart = go.Figure(data=bar_chart_content, layout=bar_chart_layout)

#plot(last_bar_chart, filename='barplottest.html', show_link=False, auto_open=True)


# =============================================================================
# Creating dashboard
# =============================================================================

app = dash.Dash()

app.layout = html.Div([dcc.Graph(id='overall-plot',figure=plot_twt_posts),
    html.Div([dcc.Graph(id='example-graph',figure=wonder_map)])
    ])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8052)
