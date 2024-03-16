# Jan 12 - add button to export
# Jan 21 - combine callbacks 1. export current view and 2. export comparison after selecting 2
# jan 21 - need to add datatable from electricity comparision #2 jupyter
import os
import io
from dash import Dash, dash_table, html
from dash import dcc
from dash import Dash, dcc, html, Input, Output, callback, State
from dash.exceptions import PreventUpdate

# from dash_extensions import Download
import pandas as pd

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')


CWD = os.getcwd()
# path if debug via vs code
path_to_file_debug = os.path.join(
    CWD, "utilisapps", "oeb_open_data", "dash_apps", "ELEC_SCORECARD.xlsx"
)
# path via python manage.py runserver

path_to_file_run = os.path.join(
    CWD, "oeb_open_data", "dash_apps", "ELEC_SCORECARD.xlsx"
)

from django_plotly_dash import DjangoDash

try:
    df_scorecard = pd.read_excel(path_to_file_debug)
except FileNotFoundError:
    df_scorecard = pd.read_excel(path_to_file_run)

# app = Dash(__name__)
app = DjangoDash("OEBSample")
app.css.append_css({"external_url": "/static/dist/semantic.min.css"})

app.layout = html.Div(
    [
        dcc.Download(id="download_Compare"),
        dcc.Download(id="download"),
        html.Button("Compare", id="Compare_button", className="ui primary button"),
        html.Button("Print", id="Print_button", className="ui primary button"),
        html.H3(
            "Press button to save data to your desktop",
            id="output-1",
            className="ui header",
        ),
        dcc.Dropdown(
            id="efficiency_dropdown1",
            options=[{"label": i, "value": i} for i in df_scorecard["dist"].unique()],
            value="1",
            className="ui selection dropdown",
        ),
        dcc.Dropdown(
            id="efficiency_dropdown2",
            options=[{"label": i, "value": i} for i in df_scorecard["dist"].unique()],
            value="1",
            className="ui selection dropdown",
        ),
        dash_table.DataTable(
            id="table",
            data=df_scorecard.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df_scorecard.columns],
            filter_action="native",
            sort_action="native",
            sort_mode="single",
            style_cell={"minWidth": 95, "maxWidth": 95, "width": 95},
            style_header={
                "backgroundColor": "red",
                "fontWeight": "bold",
                "border": "3px solid green",
            },
            style_data={"border": "3px solid blue"},
            page_size=10,
            # style_as_list_view=True,
        ),
        #                 style_cell_conditional=[
        #                     {'if': {'column_id': 'dist'},
        #                      'width': '30%'},
        #                     {'if': {'column_id': 'connections'},
        #                      'width': '30%'}],
    ],
    className="ui container",
)


@app.callback(
    Output(component_id="download_Compare", component_property="data"),
    Input(component_id="Compare_button", component_property="n_clicks"),
    State("table", "derived_virtual_data"),
    State(component_id="efficiency_dropdown1", component_property="value"),
    State(component_id="efficiency_dropdown2", component_property="value"),
    prevent_initial_call=True,
)
def download_as_csv(n_clicks, table_data, efficiency_value1, efficiency_value2):
    df_scorecard_comp = pd.DataFrame.from_dict(table_data)
    df_scorecard_comp["new col"] = "temp"  # test
    Compare_co = [efficiency_value1, efficiency_value2]
    print(Compare_co)
    df_scorecard_comp = df_scorecard[df_scorecard["dist"].isin(Compare_co)]
    df_scorecard_comp = df_scorecard_comp.T

    if not n_clicks:
        raise PreventUpdate
    download_buffer = io.StringIO()
    df_scorecard_comp.to_csv(download_buffer, index=False)
    download_buffer.seek(0)
    return dict(content=download_buffer.getvalue(), filename="Test_filename.csv")


# -----Callback to print all---------------------------
@app.callback(
    Output(component_id="download", component_property="data"),  # derived_virtual_data
    Input(component_id="Print_button", component_property="n_clicks"),
    State("table", "derived_virtual_data"),
    prevent_initial_call=True,
)
def download_as_csv(n_clicks, table_data):
    df = pd.DataFrame.from_dict(table_data)
    if not n_clicks:
        raise PreventUpdate
    download_buffer = io.StringIO()
    df.to_csv(download_buffer, index=False)
    download_buffer.seek(0)
    return dict(content=download_buffer.getvalue(), filename="Test_filename.csv")


if __name__ == "__main__":
    app.run(port=8051, debug=True)
