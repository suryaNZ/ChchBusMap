import folium
import pandas as pd
import metro_api
from flask import Flask, render_template_string
import time
import threading

# map setup

data = metro_api.retrieve_data()
df = pd.DataFrame(
    {
        'Properties':[entity.line_no for entity in data],
        'Latitude':[entity.pos.lat for entity in data],
        'Longitude':[entity.pos.lon for entity in data]
    }
)
m = folium.Map(location=[-43.620609283447266,172.48358154296875], tiles="OpenStreetMap", zoom_start=12)

line_colors = {
    'Oa': "green",
    'Oc': "green",
    '1': "lightblue",
    '3': "purple",
    '5': "yellow",
    '7': "orange",
    '8': "pink",
    '27': "orange",
    '29': "darkblue",
    '44': "blue",
    '60': "pink",
    '80': "gray",
    '81': "lightred",
    '86': "lightgreen",
    '91': "darkgreen",
    '92': "brown",
    '95': "red",
    '97': "purple",
    '100': "lightgray",
    '107': "cadetblue",
    '120': "yellow",
    '125': "green",
    '130': "darkred",
    '135': "green",
    '140': "blue",
    '155': "purple",
    '820': "green",
}

# for i in range(0,len(df)):
#     folium.Marker(
#       location = [df.iloc[i]['Latitude'], df.iloc[i]['Longitude']],
#       popup = df.iloc[i]['Properties'],
#       icon = folium.Icon(
#           color = 'blue',
#         #   icon_color = 'white',
#           icon_color = line_colors.get(df.iloc[i]['Properties'], "white"),
#           icon = 'bus-simple',
#           prefix = 'fa'
#       )
#    ).add_to(m)



# browser stuff

updating = False
rendering = False

app = Flask(__name__)

@app.route("/")
def fullscreen():
    global rendering
    while updating:
        pass
    rendering = True
    rendered = m.get_root().render()
    rendering = False
    print(rendered)
    return rendered

def run_app():
    app.run(debug=False, threaded=True)

def update_map():
    global updating
    while(True):
        global m
        data = metro_api.retrieve_data()
        df = pd.DataFrame(
            {
                'Properties':[entity.line_no for entity in data],
                'Latitude':[entity.pos.lat for entity in data],
                'Longitude':[entity.pos.lon for entity in data]
            }
        )
        m = folium.Map(location=[-43.620609283447266,172.48358154296875], tiles="OpenStreetMap", zoom_start=12)
        while rendering: pass
        print("updating")
        updating = True
        for i in range(0,len(df)):
            folium.Marker(
            location = [df.iloc[i]['Latitude'], df.iloc[i]['Longitude']],
            popup = df.iloc[i]['Properties'],
            icon = folium.Icon(
                color = 'blue',
                #   icon_color = 'white',
                icon_color = line_colors.get(df.iloc[i]['Properties'], "white"),
                icon = 'bus-simple',
                prefix = 'fa'
            )
        ).add_to(m)
        
        updating = False
        time.sleep(5)

if __name__ == "__main__":
    first_thread = threading.Thread(target = run_app)
    second_thread = threading.Thread(target = update_map)
    first_thread.start()
    second_thread.start()