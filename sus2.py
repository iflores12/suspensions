import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.charts import Scatter, output_file, show
from bokeh.layouts import widgetbox, row
from bokeh.models.widgets import Select
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import HoverTool, BoxSelectTool, ColumnDataSource
from collections import OrderedDict

suspensionsByRace = pd.read_csv("suspensionsratebyrace.csv")


def create_graph():
    df = suspensionsByRace[(suspensionsByRace["Race/Ethnicity"] == select.value) | (suspensionsByRace["Race/Ethnicity"] == select2.value)]
    x= df.groupby(['District'])
    new_df = abs(x.Value.apply(lambda x: x.iloc[1] - x.iloc[0])).sort_values(ascending=False).index
    z=list(new_df)

    df.is_copy = False
    sorterIndex = dict(zip(z,range(len(z))))
    df['District_rank'] = df['District'].map(sorterIndex)

    df.sort_values(['District_rank', 'District'], \
            ascending = [True, True], inplace = True)
    df.drop('District_rank', 1, inplace = True)


    x_name = "District"
    y_name = "Value"
    source = ColumnDataSource(
            data=dict(
                x=df['District'],
                y=df['Value'],
                color= df['Race/Ethnicity']
            )
        )


    r = list(df["District"])
    r = r[::2]
    rLength = len(r)

    f = list(range(rLength+1))

    f.pop(0)

    hover = HoverTool(
            tooltips=[
                ("District", "@x"),
                ("Race", "@color")
            ]
        )
    race1 = df['Value'][df["Race/Ethnicity"] == select.value]
    race2 = df['Value'][df["Race/Ethnicity"] == select2.value]

    colormap = {'Black or African American': 'red', 'White': 'green', "Asian": 'blue', "Native Hawaiian or Other Pacific Islander": 'black', "Two or More Races": 'yellow', "Hispanic or Latino of any race": 'orange', "American Indian or Alaska Native": 'purple'}
    colors = [colormap[x] for x in df['Race/Ethnicity']]

    plot = figure(plot_height=600, plot_width=700, title="Suspensions", x_range=r, tools=[hover])
    plot.circle(x='x', y='y',source=source, size=7, color=colors, alpha=.5)
    plot.xaxis.visible = None
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    plot.segment(x0=f, y0=race2, x1=f,
                y1=race1, color="black", alpha=.25,
                line_width=2)

    return plot

def update(attr, old, new):
    layout.children[1] = create_graph()

select = Select(title="Option:", value="White", options=["Asian", "Native Hawaiian or Other Pacific Islander ", "White", "Two or More Races", "Hispanic or Latino of any race", "American Indian or Alaska Native", "Black or African American"])
select.on_change('value', update)

select2 = Select(title="Option:", value="Black or African American", options=["Asian", "Native Hawaiian or Other Pacific Islander ", "White", "Two or More Races", "Hispanic or Latino of any race", "American Indian or Alaska Native", "Black or African American"])
select2.on_change('value', update)

controls = widgetbox([select, select2], width=500)
layout = row(controls, create_graph())

curdoc().add_root(layout)
curdoc().title = "Suspensions"
