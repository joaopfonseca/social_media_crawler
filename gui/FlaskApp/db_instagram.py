#!/usr/bin/env python

from datetime import datetime
import os

#querying
import pandas as pd
import numpy as np

#plotting
#from plotly.offline import plot #to save graphs as html files, useful when testing
import plotly.graph_objs as go

#dashboarding
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

mapbox_access_token = 'pk.eyJ1Ijoiam9hb2ZvbnNlY2EiLCJhIjoiY2picXB3cDVvMDczYjJ3bzBxNDV3dGI0MSJ9.XpQDNjTuMAM-xckGln0KrA'


app = dash.Dash()
#app.css.append_css({"external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css"})



kw_filter= open('support/active_keyword', 'r')
header_keyword=kw_filter.readline()
keyword = header_keyword.rstrip()
kw_filter.close()

path = '../../Web_Crawler/_data/'
i = open(path + '%s_instagram_posts.csv' % keyword, 'r')

ig_df = pd.read_csv(i)

def drop_minutes_and_seconds(olddate):
    new_date = datetime.fromtimestamp(olddate).replace(minute=0, second=0, microsecond=0)
    return new_date

ig_df['date'] = ig_df['taken_at'].apply(drop_minutes_and_seconds)
ig_df.sort_values(['date'], ascending=False)

#yvalues_ig_hist1 = ig_df[['date']].groupby('date').size()
#
#xvalues = []
#for value in ig_df['date']:
#    if value not in xvalues:
#        xvalues.append(value)
#yvalues = []
#for date in xvalues:
#    yvalues.append(yvalues_ig_hist1[date])


#plotting Ig posts
diff = (max(ig_df['date'])-min(ig_df['date']))

number_of_bins= (diff.days+1)*24
#first_ig_histogram = [go.Scatter(x=xvalues, y=yvalues)]
ig_histogram = [go.Histogram(x=ig_df['date'], nbinsx=number_of_bins)]

hist_configuration= go.Layout(title='Instagram posts associated to keyword \'%s\'' % keyword, xaxis=dict(title='Hours'), yaxis=dict(title='Count'))
plot_ig_posts = go.Figure(data=ig_histogram, layout=hist_configuration)
#flnm_posts_ig_histogram= keyword + '_posts_ig_histogram.html'
#plot(plot_ig_posts, filename=flnm_posts_ig_histogram, show_link=False, auto_open=False)

i.close()

# =============================================================================
# plotting geomap
# =============================================================================


lon=[]
for coord in ig_df['lng']:
    lon.append(coord)

lat=[]
for coord in ig_df['lat']:
    lat.append(coord)

#size=

data = go.Data([
        go.Scattermapbox(
                lat=ig_df['lat'],
                lon=ig_df['lng'],
                mode='markers',
#                marker=go.Marker(
#                        size=[endpt_size] + [4 for j in range(len(steps) - 2)] + [endpt_size])
                text=ig_df['caption_text']
                )
        ])

layout = go.Layout(
    title='Location of Posts',
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
#plot(wonder_map, filename='scatterplottest.html', show_link=False, auto_open=True)

# =============================================================================
# last plot
# =============================================================================

comments_data_datecount = ig_df.groupby('date').agg({'comment_count': np.sum}).reset_index()
ig_df['postcount']=ig_df['date']
posts_data_datecount = ig_df.groupby('date').agg({'postcount': np.count_nonzero}).reset_index()

comments_plot= go.Bar(x=comments_data_datecount['date'], y=comments_data_datecount['comment_count'], name='Comments')
posts_plot= go.Bar(x=posts_data_datecount['date'] ,y=posts_data_datecount['postcount'], name='Posts' )
bar_chart_layout= go.Layout(title='Number of comments relative to posts', xaxis=dict(title='Days'), yaxis=dict(title='Count'))
bar_chart_content = [posts_plot,comments_plot]
last_bar_chart = go.Figure(data=bar_chart_content, layout=bar_chart_layout)

#plot(last_bar_chart, filename='barplottest.html', show_link=False, auto_open=True)


# =============================================================================
# Creating dashboard
# =============================================================================


app.layout = html.Div([
#    html.H1('Hello Dash'),
#    html.Div('''Dash: A web application framework for Python.'''),
    dcc.Graph(id='overall-plot',figure=last_bar_chart),
    html.Div([
            dcc.Graph(id='example-graph',figure=wonder_map)
            ], style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
            dcc.Graph(id='whatsthisevenfor',figure=plot_ig_posts)
            ], style={'width': '49%', 'display': 'inline-block'})
    ])



if __name__ == '__main__':
    app.server.run(host='0.0.0.0', port=8051)
