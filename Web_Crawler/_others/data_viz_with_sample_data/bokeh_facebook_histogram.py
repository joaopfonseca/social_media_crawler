
from os.path import dirname, join


#for querying and graph plotting purposes
import pandas as pd

#for plotting purposes
from bokeh.models import ColumnDataSource, Div
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.io import curdoc

#menus
from bokeh.layouts import layout, widgetbox
from bokeh.models.widgets import Dropdown
from bokeh.models.widgets import TextInput




twitter_search = 'cascais'
page_id = 'cascais'


f = open('%s_facebook_statuses.csv' % page_id, 'r')
t = open('%s_tweets.csv' % twitter_search, 'r')

#some querying/ETL here
posts_table = pd.read_csv(f)
posts_table['date'] = pd.to_datetime(posts_table['status_published'])
posts_table['year'] = posts_table['date'].dt.year
posts_table['month'] = posts_table['date'].dt.month
posts_table['-'] = '-'
posts_table['yearmonth'] = pd.to_datetime(posts_table['year'].astype(str) + posts_table['-'] + posts_table['month'].astype(str)).astype(str)

posts_table['fb_posts'] = posts_table['status_id']



tweets_table = pd.read_csv(t)
tweets_table['date'] = pd.to_datetime(tweets_table['created_at'])
#tweets_table['year'] = tweets_table['date'].dt.year
#tweets_table['month'] = tweets_table['date'].dt.month
tweets_table['tweets'] = tweets_table['tweet_id']


#assembling the final tables
df_facebook_posts = posts_table[['fb_posts','yearmonth']].groupby('yearmonth')

#df_tweets = tweets_table[['tweets','date']].groupby('date').agg({'tweets': np.size})










director = TextInput(title="textinput test")

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example

inputs = widgetbox(director, sizing_mode=sizing_mode)



#plotting the histogram here
output_file('facebook_posts_histogram.html')


source = ColumnDataSource(df_facebook_posts)
p = figure(plot_height=350, x_range=df_facebook_posts)
p.vbar(x='yearmonth', top='fb_posts_count', width=1, line_color="white", source=source)

p.y_range.start = 0



desc = Div(text=open(join(dirname(__file__), "description.html")).read(), width=800)
l = layout([
    [desc],
    [inputs, p]
], sizing_mode=sizing_mode)

curdoc().add_root(l)
curdoc().title = "Movies"

show(l)




###################################
#dropdown menu
"""
menu = [("Item 1", "item_1"), ("Item 2", "item_2"), None, ("Item 3", "item_3")]
dropdown = Dropdown(label="Dropdown button", button_type="warning", menu=menu)

show(widgetbox(dropdown))
"""
####################################


#Text Input
"""
text_input = TextInput(value="default", title="Label:")

show(widgetbox(text_input))
"""



"""
def my_text_input_handler(attr, old, new):
    print("Previous label: " + old)
    print("Updated label: " + new)

text_input = bokeh.my_text_input_handler(value="default", title="Label:")
text_input.on_change("value", my_text_input_handler)
"""

#show(p)
