from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://docs.google.com/spreadsheets/d/1zWZ1gZYvXqAuRoARqLO5CAWr2wMfEtW8mJx02l38leg/export?format=csv'
ex_df = pd.read_csv(url)

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://docs.google.com/spreadsheets/d/1zWZ1gZYvXqAuRoARqLO5CAWr2wMfEtW8mJx02l38leg/export?format=csv'
    ex_df = pd.read_csv(url)

    lat = list(ex_df['Latitude'])
    lon = list(ex_df['Longitude'])
    name = list(ex_df['Artist/Program'])
    title = list(ex_df['Title'])
    category = list(ex_df['Category'])
    loc = list(ex_df['Location'])

    color_map = {
        'Community Engaged': '#65c786',
        'Beautification': '#e0779a',
        'Historical': '#914c0c'
    }

    colors = [color_map.get(cat, '#000000') for cat in category]

    text = [
        f"Name: {n}<br>Title: <i>{t}</i><br>Category: {c}<br>Location: {l}"
        for n, t, c, l in zip(name, title, category, loc)
    ]

    fig = go.Figure(go.Scattermapbox(
      lat=lat,
      lon=lon,
      mode='markers',
      marker=go.scattermapbox.Marker(
          size=9,
          color=colors
      ),
      text=text
    ))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken='pk.eyJ1IjoiczRicmlhIiwiYSI6ImNsemhqOTRmeDA1Zjcyam9mM2ZsY3BuazIifQ.OsCFi5lAtP4ReDHMfNtcCQ',
            bearing=0,
            center=dict(
                lat=40.730610,
                lon=-73.935242
            ),
            pitch=0,
            zoom=9
        ),
    )

    # Convert Plotly figure to JSON
    graphJSON = pio.to_json(fig)

    return render_template('index.html', graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
