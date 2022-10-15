from msilib.schema import tables
from dash import Dash, dcc, html, Input, Output
import os
import plotly.express as px
import pandas as pd
import geopy.distance
import numpy as np

app = Dash(__name__)

colors = {
    'background': 'rgba(0,0,0,0)',
    'text': 'white'
}

df = pd.read_csv('https://github.com/marleen2511/horse-racing-dash/blob/50407d5091aee3ff6702f34fd075a88402cd9572/nyra_tracking_table.csv')
df_start = pd.read_csv('https://github.com/marleen2511/horse-racing-dash/blob/50407d5091aee3ff6702f34fd075a88402cd9572/nyra_start_table.csv')
df_start.columns =['track_id', 'race_date', 'race_number', 'program_number', 'weight_carried', 'jockey', 'odds', 'position_at_finish']
df_start["program_number"] = pd.DataFrame([''.join(filter(str.isdigit, x)) for x in df_start['program_number']]).astype(str).astype(int)

api_token = "pk.eyJ1IjoibWFybGVlbjI1MTEiLCJhIjoiY2w5NGcxOW8wMXo2bDNwcDJyd3owbHFidCJ9.xxRU7jqFjwpMWClTY1wxoA"

app.layout = html.Div([
                html.H2(["HORSE RACING DASHBOARD"], id='title-1'),
                html.Div([
                    html.Div([
                        html.H3(["Track ID"], id='dropdown-title-2'),
                        dcc.Dropdown(df_start["track_id"].unique(), ["AQU"], multi=True,  placeholder="Select...", id="dropdown-1")], className="drop"),
                    html.Div([
                        html.H3("Race Date", id='dropdown-title-3'),
                        dcc.Dropdown([], ["2019-01-01"], id='dropdown-2', multi=True,  placeholder="Select...")], className="drop"),
                    html.Div([
                        html.H3(["Race Number"], id='dropdown-title-4'),
                        dcc.Dropdown([], 1,
                        id='dropdown-3', multi=False, placeholder="Select...")], className="drop"),
                    html.Div([
                        html.H3(["Program Number"], id='dropdown-title-5'),
                        dcc.Dropdown([], [1],
                        id='dropdown-4', multi=True,  placeholder="Select...")], className="drop")
                    ], id="drop-1"),
                html.Div([
                    html.Div([
                        html.H3(["Ranking"], id='dropdown-title-6'),
                        dcc.Dropdown([], [], multi=True,  placeholder="Select...", id="dropdown-5")], className="drop"),
                    html.Div([
                        html.H3(["Jockey"], id='dropdown-title-7'),
                        dcc.Dropdown([], [],
                        id='dropdown-6', multi=True,   placeholder="Select...")], className="drop"),
                    html.Div([
                        html.H3(["Weight carried"], id='dropdown-title-8'),
                        dcc.Dropdown([], [],
                        id='dropdown-7', multi=True,  placeholder="Select...")], className="drop"),
                    html.Div([
                        html.H3(["Odds"], id='dropdown-title-9'),
                        dcc.Dropdown([], [],
                        id='dropdown-8', multi=True,  placeholder="Select...")], className="drop")
                    ], id="drop-2"),
                dcc.Loading(
                    className='loader',
                    id="loading-1", type="default", color="#ffffff", children=html.Div([
                    dcc.Graph(
                        className='graph',
                        id='speed-mean',
                    )], id="loader-1")),
                dcc.Loading(
                    className='loader',
                    color="#ffffff",
                    id="loading-2", 
                    type="default", 
                    children=html.Div([
                    dcc.Graph(
                        className='graph',
                        id='tactics-mean',
                    )], id="loader-2")),
                dcc.Loading(
                    className='loader',
                    id="loading-3", type="default", color="#ffffff", children=html.Div([
                    dcc.Graph(
                        className='graph',
                        id='speed',
                    )], id="loader-3")),
                dcc.Loading(
                    className='loader',
                    color="#ffffff",
                    id="loading-4", 
                    type="default", 
                    children=html.Div([
                    dcc.Graph(
                        className='graph',
                        id='tactics',
                    )], id="loader-4")),
                dcc.Loading(
                    className='loader',
                    color="#ffffff",
                    id="loading-5", type="default", children=html.Div([
                    dcc.Graph(
                        className='map',
                        id='map',
                    )], id="loader-5"))
            ],  style={'margin': 'auto', 'height': '480vh', 'width': '100vw'})


@app.callback(
    Output("dropdown-2", "options"),
    Input("dropdown-1", "value"))
def set_date_options(track):
    df_start = pd.read_csv('https://github.com/marleen2511/horse-racing-dash/blob/50407d5091aee3ff6702f34fd075a88402cd9572/nyra_start_table.csv')
    df_start.columns =['track_id', 'race_date', 'race_number', 'program_number', 'weight_carried', 'jockey', 'odds', 'position_at_finish']
    df_start["program_number"] = pd.DataFrame([''.join(filter(str.isdigit, x)) for x in df_start['program_number']]).astype(str).astype(int)
    print([i for i in df_start[df_start["track_id"].isin(track)]["race_date"].unique()])
    return [i for i in df_start[df_start["track_id"].isin(track)]["race_date"].unique()]

@app.callback(
    Output("dropdown-2", "value"),
    Input("dropdown-2", "options"))
def set_date_value(options_race_date):
    return [options_race_date[0]]

@app.callback(
    Output("dropdown-3", "options"),
    Input("dropdown-2", "value"),
    Input("dropdown-1", "value"))
def set_number_options(race_date, track):
    return df_start[df_start["track_id"].isin(list(track)) & df_start["race_date"].isin(list(race_date))]["race_number"].unique()

@app.callback(
    Output("dropdown-3", "value"),
    Input("dropdown-3", "options"))
def set_number_value(options_race_number):
    return options_race_number[0]

@app.callback(
    Output("dropdown-4", "options"),
    Input("dropdown-3", "value"),
    Input("dropdown-2", "value"),
    Input("dropdown-1", "value"))
def set_program_options(race_number, race_date, track):
    race_number = [race_number]
    return df_start[df_start["track_id"].isin(list(track)) & df_start["race_date"].isin(list(race_date)) & df_start["race_number"].isin(list(race_number))]["program_number"].unique()

@app.callback(
    Output("dropdown-4", "value"),
    Input("dropdown-4", "options"))
def set_program_value(options_program_number):
    return [options_program_number[0]]


@app.callback(
    Output("dropdown-5", "options"),
    Output("dropdown-6", "options"),
    Output("dropdown-7", "options"),
    Output("dropdown-8", "options"),
    Input("dropdown-4", "value"),
    Input("dropdown-3", "value"),
    Input("dropdown-2", "value"),
    Input("dropdown-1", "value"))
def set_other_options(program_number, race_number, race_date, track):
    race_number = [race_number]
    return df_start[df_start["track_id"].isin(list(track)) & df_start["race_date"].isin(list(race_date)) & df_start["race_number"].isin(list(race_number))  & df_start["program_number"].isin(program_number)]["position_at_finish"].unique(),\
    df_start[df_start["track_id"].isin(list(track)) & df_start["race_date"].isin(list(race_date)) & df_start["race_number"].isin(list(race_number))  & df_start["program_number"].isin(program_number)]["jockey"].unique(),\
    df_start[df_start["track_id"].isin(list(track)) & df_start["race_date"].isin(list(race_date)) & df_start["race_number"].isin(list(race_number))  & df_start["program_number"].isin(program_number)]["weight_carried"].unique(),\
    df_start[df_start["track_id"].isin(list(track)) & df_start["race_date"].isin(list(race_date)) & df_start["race_number"].isin(list(race_number))  & df_start["program_number"].isin(program_number)]["odds"].unique()

@app.callback(
    Output("dropdown-5", "value"),
    Output("dropdown-6", "value"),
    Output("dropdown-7", "value"),
    Output("dropdown-8", "value"),
    Input("dropdown-8", "options"),
    Input("dropdown-7", "options"),
    Input("dropdown-6", "options"),
    Input("dropdown-5", "options"))
def set_other_value(options_odds, options_weight, options_jockey, options_ranking):
    return [options_ranking][0], [options_jockey][0], [options_weight][0], [options_odds][0]

@app.callback(
    Output("speed-mean", "figure"),
    Output("tactics-mean", "figure"),
    Output("speed", "figure"),
    Output("tactics", "figure"), 
    Output("map", "figure"), 
    Input("dropdown-1", "value"),
    Input("dropdown-2", "value"),
    Input("dropdown-3", "value"),
    Input("dropdown-4", "value"))
def update_acc_chart(track, race_date, race_number, program_number):
    print([track, race_date, [race_number], program_number])
    race_number = [race_number]
    if ((len(track) > 0) & (len(race_date) > 0) & (len(str(race_number)) > 0) & (len(str(program_number)) > 0 )):
        df = pd.read_csv('https://github.com/marleen2511/horse-racing-dash/blob/50407d5091aee3ff6702f34fd075a88402cd9572/nyra_tracking_table.csv')
        df_start = pd.read_csv('https://github.com/marleen2511/horse-racing-dash/blob/50407d5091aee3ff6702f34fd075a88402cd9572/nyra_start_table.csv')
        df_start.columns =['track_id', 'race_date', 'race_number', 'program_number', 'weight_carried', 'jockey', 'odds', 'position_at_finish']
        df_start["program_number"] = pd.DataFrame([''.join(filter(str.isdigit, x)) for x in df_start['program_number']]).astype(str).astype(int)
        df_start = df_start[df_start["track_id"].isin(list(track)) & df_start["race_date"].isin(list(race_date)) & df_start["race_number"].isin(list([race_number]))].reset_index(drop=True)
        
        df_plot = pd.DataFrame()
        for t in track:
            df = df[df["track_id"] == t]
            for rd in race_date: 
                df = df[df["race_date"] == rd]
                for rn in race_number:
                    df = df[df["race_number"] == rn]
                    df = df.groupby(["program_number"])
                    lat = df["latitude"].apply(pd.DataFrame).reset_index(drop=True)
                    long = df["longitude"].apply(pd.DataFrame).reset_index(drop=True)
                    # average acceleration over horses
                    lat_profile_race = pd.DataFrame()
                    for i in lat.columns:
                        lat_profile_race= lat_profile_race.assign(**{str(i): lat[:][i].dropna().reset_index(drop=True)})
                    long_profile_race = pd.DataFrame()
                    for i in long.columns:
                        long_profile_race= long_profile_race.assign(**{str(i): long[:][i].dropna().reset_index(drop=True)})
                    # take mean over horses => average of race
                    lat_profile_race_mean = lat_profile_race.mean(axis=1)
                    long_profile_race_mean = long_profile_race.mean(axis=1)
                    for pn in program_number:
                        difference_lat_profile = lat_profile_race.sub(lat_profile_race_mean, axis='index')
                        difference_long_profile = long_profile_race.sub(long_profile_race_mean, axis='index')
                        for i in range(0,len(difference_long_profile)-1):
                            lat_profile_race.columns = [x.strip() for x in lat_profile_race.columns.tolist()]
                            long_profile_race.columns = [x.strip() for x in long_profile_race.columns.tolist()]
                            difference_lat_profile.columns = [x.strip() for x in difference_lat_profile.columns.tolist()]
                            difference_long_profile.columns = [x.strip() for x in difference_long_profile.columns.tolist()]
                            df_plot =  df_plot.append({"Time": i, "Program Number": str(pn), "Speed_mean": geopy.distance.distance([lat_profile_race_mean[i], long_profile_race_mean[i]],[lat_profile_race_mean[i+1], long_profile_race_mean[i+1]]).m/0.25, "Acceleration_mean": geopy.distance.distance([lat_profile_race_mean[i], long_profile_race_mean[i]],[lat_profile_race_mean[i+1], long_profile_race_mean[i+1]]).m/pow(0.25,2), "Lat": lat_profile_race[str(pn)][i], "Lon": long_profile_race[str(pn)][i], "Speed": geopy.distance.distance([difference_lat_profile[str(pn)][i], difference_long_profile[str(pn)][i]],[difference_lat_profile[str(pn)][i+1], difference_long_profile[str(pn)][i+1]]).m/0.25, "Acceleration": geopy.distance.distance([difference_lat_profile[str(pn)][i], difference_long_profile[str(pn)][i]],[difference_lat_profile[str(pn)][i+1], difference_long_profile[str(pn)][i+1]]).m/pow(0.25,2)}, ignore_index=True)
        for i, value in enumerate(df_plot.Speed_mean):
            if value > 20:
                   df_plot.Speed_mean[i] = df_plot.Speed_mean[i-1]
        for i, value in enumerate(df_plot.Speed):
            if value > 20:
                   df_plot.Speed[i] = df_plot.Speed[i-1]
        for i, value in enumerate(df_plot.Acceleration_mean):
            if value > 100:
                   df_plot.Acceleration_mean[i] = df_plot.Acceleration_mean[i-1]
        for i, value in enumerate(df_plot.Acceleration):
            if value > 100:
                   df_plot.Acceleration[i] = df_plot.Acceleration[i-1]
        map = px.scatter_mapbox(df_plot, lat="Lat", lon="Lon", size="Speed", color="Program Number", height=600, size_max=15, zoom=15)    
        map.update_layout(plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
            font_size=16,  
            title={'xanchor': 'center','yanchor': 'top', 'y':0.9, 'x':0.5,}, 
            title_font_size = 24, 
            mapbox_accesstoken=api_token, 
            mapbox_style = "mapbox://styles/mapbox/dark-v10")  
        fig_speed_mean = px.line(df_plot, x="Time", y="Speed_mean", color='Program Number')
        fig_acc_mean = px.line(df_plot, x="Time", y="Acceleration_mean", color='Program Number')
        fig_speed = px.line(df_plot, x="Time", y="Speed", color='Program Number')
        fig_acc = px.line(df_plot, x="Time", y="Acceleration", color='Program Number')
        fig_speed_mean.update_xaxes(title_text="", showgrid=False, showticklabels=False, row=1, col=1)
        fig_speed_mean.update_yaxes(title_text="Speed Mean of the Race", showgrid=False, row=1, col=1)
        fig_acc_mean.update_xaxes(title_text="Measure Point", showgrid=False, row=1, col=1)
        fig_acc_mean.update_yaxes(title_text="Acceleration Mean of the Race", showgrid=False, row=1, col=1)
        fig_speed.update_xaxes(title_text="", showgrid=False, showticklabels=False, row=1, col=1)
        fig_speed.update_yaxes(title_text="Speed(difference from mean)", showgrid=False, row=1, col=1)
        fig_acc.update_xaxes(title_text="Measure Point", showgrid=False, row=1, col=1)
        fig_acc.update_yaxes(title_text="Acceleration (difference from mean)", showgrid=False, row=1, col=1)
        fig_speed_mean.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )
        fig_acc_mean.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )
        fig_speed.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )
        fig_acc.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )
        return fig_speed_mean, fig_acc_mean, fig_speed, fig_acc, map


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(host='0.0.0.0', port=port)
