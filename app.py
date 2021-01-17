from flask import Flask, render_template, url_for, current_app, request
from flask_restful import Resource,Api

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

from model.helloworld import HelloWorld
from model.todo_simple import TodoSimple

import matplotlib.pyplot as plt
import numpy as np
import matplotlib, mpld3

import pandas as pd
import geopandas as gpd


app = Flask(__name__)
api = Api(app)

app.secret_key = '12345678'
#Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

api.add_resource(HelloWorld, '/hw')
api.add_resource(TodoSimple, '/todo/<string:todo_id>')


@app.route('/dbtest')
def dbinsert():
	engine = create_engine('postgresql://app_user:app_password@localhost:5432/weather')
	db = scoped_session(sessionmaker(bind=engine))
	engine.execute('INSERT INTO "people" (id, name) VALUES (1,"raw1")')
	db.commit()
	return "DB Ran"

@app.route('/')
def index():
		# Don't allow matplotlib to render in different thread
	matplotlib.use('Agg')

	#reading the file stored in variable fp and map_df
	#reading the file stored in variable fp
	map_df = gpd.read_file("static/data/District_boundary/District_Boundary.shp")
	df = gpd.read_file("static/data/District_boundary/District_Boundary.shp")

	#selecting the columns required
	df = df[["DIST_NAME","POPULATION"]]
	#renaming the column name
	data_for_map = df.rename(index=str, columns={"DIST_NAME": "DISTRICT","POPULATION": "POP"})
	# print(data_for_map.head())

	# joining the geodataframe with the cleaned up csv dataframe
	merged = map_df.set_index("DIST_NAME").join(data_for_map.set_index("DISTRICT"))
	#.head() returns the top 5(by default ) lines of the dataframe
	
	#CREATE MAP
	# set a variable that will call whatever column we want to visualise on the map
	variable = "POP"
	# set the range for the choropleth
	vmin, vmax = 120, 220
	# create figure and axes for Matplotlib
	fig, ax = plt.subplots(1, figsize=(10, 6))

	merged.plot(column=variable, cmap="BuGn", linewidth=0.8, ax=ax, edgecolor="0.8")


	# BEAUTIFY MAP
	# remove the axis
	ax.axis("off")
	# add a title
	ax.set_title("Population of Rajasthan", fontdict={"fontsize": "25", "fontweight" : "3"})
	# create an annotation for the data source
	ax.annotate("Source: Rajasthan Datastore, 2019",xy=(0.1, .08), xycoords="figure fraction", horizontalalignment="left", verticalalignment="top", fontsize=12, color="#555555")

	# ADD COLOR BAR
	# Create colorbar as a legend
	sm = plt.cm.ScalarMappable(cmap="BuGn", norm=plt.Normalize(vmin=vmin, vmax=vmax))
	# empty array for the data range
	sm._A = []
	# add the colorbar to the figure
	cbar = fig.colorbar(sm)
	#saving our map as .png file.
	#fig.savefig(‘map_export.png’, dpi=300)


	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# ax.plot([1, 2, 3, 4], [10, 20, 25, 30], color='lightblue', linewidth=3)
	# ax.scatter([0.3, 3.8, 1.2, 2.5], [11, 25, 9, 26], color='darkgreen', marker='^')
	# ax.set_xlim(0.5, 4.5)


	# Convert figure to substring
	html_str = mpld3.fig_to_html(fig)

	return render_template('index.html', value=html_str)

@app.route('/dash')
def dash():
	return render_template('dash.html')

@app.route('/indexng')
def index_ng():
	return render_template('indexng.html')

@app.route('/plot')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


# D3 Testing 1
@app.route('/d3test')
def d3test():
	# Don't allow matplotlib to render in different thread
	matplotlib.use('Agg')

	#reading the file stored in variable fp and map_df
	#reading the file stored in variable fp
	map_df = gpd.read_file("static/data/District_boundary/District_Boundary.shp")
	df = gpd.read_file("static/data/District_boundary/District_Boundary.shp")

	#selecting the columns required
	df = df[["DIST_NAME","POPULATION"]]
	#renaming the column name
	data_for_map = df.rename(index=str, columns={"DIST_NAME": "DISTRICT","POPULATION": "POP"})
	# print(data_for_map.head())

	# joining the geodataframe with the cleaned up csv dataframe
	merged = map_df.set_index("DIST_NAME").join(data_for_map.set_index("DISTRICT"))
	#.head() returns the top 5(by default ) lines of the dataframe
	
	#CREATE MAP
	# set a variable that will call whatever column we want to visualise on the map
	variable = "POP"
	# set the range for the choropleth
	vmin, vmax = 120, 220
	# create figure and axes for Matplotlib
	fig, ax = plt.subplots(1, figsize=(10, 6))

	merged.plot(column=variable, cmap="BuGn", linewidth=0.8, ax=ax, edgecolor="0.8")


	# BEAUTIFY MAP
	# remove the axis
	ax.axis("off")
	# add a title
	ax.set_title("Population of Rajasthan", fontdict={"fontsize": "25", "fontweight" : "3"})
	# create an annotation for the data source
	ax.annotate("Source: Rajasthan Datastore, 2019",xy=(0.1, .08), xycoords="figure fraction", horizontalalignment="left", verticalalignment="top", fontsize=12, color="#555555")

	# ADD COLOR BAR
	# Create colorbar as a legend
	sm = plt.cm.ScalarMappable(cmap="BuGn", norm=plt.Normalize(vmin=vmin, vmax=vmax))
	# empty array for the data range
	sm._A = []
	# add the colorbar to the figure
	cbar = fig.colorbar(sm)
	#saving our map as .png file.
	#fig.savefig(‘map_export.png’, dpi=300)


	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# ax.plot([1, 2, 3, 4], [10, 20, 25, 30], color='lightblue', linewidth=3)
	# ax.scatter([0.3, 3.8, 1.2, 2.5], [11, 25, 9, 26], color='darkgreen', marker='^')
	# ax.set_xlim(0.5, 4.5)


	# Convert figure to substring
	html_str = mpld3.fig_to_html(fig)

	return render_template('d3test.html', value=html_str)


if __name__ == '__main__':
	app.run(debug=True)
