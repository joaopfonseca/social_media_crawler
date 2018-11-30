
import datetime

#for querying and graph plotting purposes
import pandas as pd

#for plotting purposes
#from plotly.offline import plot #to save graphs as html files, useful when testing
import plotly.graph_objs as go

#for the dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html


with open('support/active_keyword', 'r') as kw_filter:
    header_keyword=kw_filter.readline()

keyword = header_keyword.rstrip()
path = '../../Web_Crawler/_data/'
f = open(path + '%s_facebook_statuses.csv' % keyword, 'r')


#querying FB posts
posts_table = pd.read_csv(f)
posts_table['date'] = pd.to_datetime(posts_table['status_published'])
posts_table['year'] = posts_table['date'].dt.year
posts_table['month'] = posts_table['date'].dt.month
posts_table = posts_table[posts_table['year'] > 2003]

#plotting FB posts
first_fb_histogram = [go.Histogram(x=posts_table['date'])]
hist_configuration= go.Layout(title='Posts associated to keyword \'%s\'' % keyword, xaxis=dict(title='Date'), yaxis=dict(title='Count'))
plot_fb_posts = go.Figure(data=first_fb_histogram, layout=hist_configuration)
#flnm_posts_fb_histogram= keyword + '_posts_fb_histogram.html'
#plot(plot_fb_posts, filename=flnm_posts_fb_histogram, show_link=False, auto_open=False)

f.close()

# =============================================================================
# creating second plot
# =============================================================================
f2 = open(path + '%s_facebook_comments.csv' % keyword, 'r')
comments_table = pd.read_csv(f2)
#formatting the one column we'll be using
comments_table['date']=pd.to_datetime(comments_table['comment_published'])

#plotting FB comments
second_fb_histogram = [go.Histogram(x=comments_table['date'])]
hist_configuration2= go.Layout(title='Comments associated to keyword \'%s\'' % keyword, xaxis=dict(title='Date'), yaxis=dict(title='Count'))
plot_fb_comments = go.Figure(data=second_fb_histogram, layout=hist_configuration2)

#flnm_comments_fb_histogram= keyword + '_comments_fb_histogram.html'
#plot(plot_fb_comments, filename=flnm_comments_fb_histogram, show_link=False, auto_open=False)

f2.close()

# =============================================================================
# creating third plot (last month analysis)
# =============================================================================

comments_last_month = comments_table[(comments_table['date']+datetime.timedelta(days=31)) > datetime.datetime.today()]
posts_last_month = posts_table[(posts_table['date']+datetime.timedelta(days=31)) > datetime.datetime.today()]

last_fb_histogram_comments = go.Histogram(x=comments_last_month['date'], name='Comments')
last_fb_histogram_posts = go.Histogram(x=posts_last_month['date'], name='Posts')

last_fb_histogram = [last_fb_histogram_comments,last_fb_histogram_posts]

hist_configuration3= go.Layout(title='Activity in pages for the last 30 days', xaxis=dict(title='Days'), yaxis=dict(title='Count'))
plot_fb_last_month = go.Figure(data=last_fb_histogram, layout=hist_configuration3)

#flnm_comments_fb_histogram= keyword + '_facebook_last_month.html'
#plot(plot_fb_comments, filename=flnm_comments_fb_histogram, show_link=False, auto_open=False)


# =============================================================================
# creating dashboard
# =============================================================================

app = dash.Dash()


app.layout = html.Div([
#    html.H1('Hello Dash'),
#    html.Div('''Dash: A web application framework for Python.'''),
    dcc.Graph(id='overall-plot',figure=plot_fb_last_month),
    html.Div([
            dcc.Graph(id='example-graph',figure=plot_fb_posts)
            ],
            style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
            dcc.Graph(id='whatsthisevenfor', figure=plot_fb_comments)
            ], style={'width': '49%', 'display': 'inline-block'})
    ])



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)
