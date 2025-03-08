# dash 
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State 
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.express as px

# utils
import mysql_utils as mysql
import mongodb_utils as mongodb
import neo4j_utils as neo4j
import traceback

# dash sytlesheets
external_stylesheets = [dbc.themes.LUX]
app = Dash(__name__, external_stylesheets=external_stylesheets)

university_dropdown_data = mysql.university_dropdown()

app.layout = dbc.Container([
    # title
    dbc.Row([
        html.Div('University Faculty Directory', className="text-primary text-center fs-3 mb-3 mt-3")
    ]),

    # university drop down
    dbc.Row([
        dcc.Dropdown(options=university_dropdown_data, value=12, id="university-dropdown")
    ], className="mb-3"),

    dbc.Row([
        # widget 1: shows how many facutly members are at each university
        dbc.Col([
            html.Div('Faculty Count', className="text-primary text-center fs-5"),
            html.Div(className="text-primary text-center fs-1", id="faculty-count")
        ], style={
            "margin-left": "10px",
            "border": "2px solid #007BFF",
            "border-radius": "10px",
            "padding": "10px",
            "height": "100px",
        }, width=2),

        # widget 2: faculty table
        dbc.Col([
            dash_table.DataTable(data=[], columns=[
                {'name': 'Name', 'id': 'Name'},
                {'name': 'Position', 'id': 'Position'},
                {'name': 'Email', 'id': 'Email'},
                {'name': 'Phone', 'id': 'Phone'},
            ],
            page_size=10,
            cell_selectable=False,
            style_cell={
                'maxWidth': '200px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'whiteSpace': 'normal'
            },
            style_table={'overflowX': 'auto'},
            id="faculty-table",
            editable=True)
        ], style={
            "margin-left": "10px",
            "border": "2px solid #007BFF",
            "border-radius": "10px",
            "padding": "10px"
        }, width=6),

        # widget 3: graph of the top 10 keywords among the faculty at a specific university 
        dbc.Col([
            html.Div('Top 10 Keywords Among Faculty', className="text-primary text-center fs-3 mb-3 mt-3"),
            dcc.Graph(id="graph")
        ], style={
            "margin-left": "10px",
            "border": "2px solid #007BFF",
            "border-radius": "10px",
            "padding": "10px"
        }, width=3),
    ], className="mb-3"),

    dbc.Row([
        # widget 4: inserting faculty in any university 
        dbc.Col([
            html.Div('Insert Faculty', className="text-primary text-center fs-3"),

            dbc.Form([
                dbc.Label("Name:"),
                dbc.Input(id='name-input', type='text', placeholder='Enter name...', required=True, className="mb-3"),
                dbc.Label("Position:"),
                dbc.Input(id='position-input', type='text', placeholder='Enter position...', required=True, className="mb-3"),
                dbc.Label("Email:"),
                dbc.Input(id='email-input', type='text', placeholder='Enter email...', required=True, className="mb-3"),
                dbc.Label("Phone #:"),
                dbc.Input(id='phone-input', type='text', placeholder='Enter phone #...', required=True, className="mb-3"),
                dbc.Label("University Affiliation"),
                dcc.Dropdown(id='university-input', options=university_dropdown_data, className="mb-3"),
                dbc.Button('Submit', id='submit-button', color='primary', className="mb-3"),
            ]),
            html.Div(id='form-submitted', className="text-primary text-center fs-5")
        ], style={
            "margin-left": "10px",
            "border": "2px solid #007BFF",
            "border-radius": "10px",
            "padding": "10px"
        }, width=2),

        # widget 5: shows each faculty's keywords and their number of publications
        dbc.Col([
            dbc.Row([
                html.Div('Select Faculty', className="text-primary text-center fs-3 mb-3 mt-3")
            ]),

            dbc.Row([
                dcc.Dropdown(options=[], id="faculty-dropdown")
            ], className="mb-3"),

            dbc.Row([
                html.Div('Faculty Keywords', className="text-primary text-center fs-3 mb-3 mt-3", style={'textDecoration': 'underline'})
            ], className="mb-3"),

            dbc.Row([
                html.Div(className="text-primary text-center fs-5", id='keyword-list')
            ], className="mb-3"),

            dbc.Row([
                html.Div('Faculty Publication Count', className="text-primary text-center fs-3 mb-3 mt-3", style={'textDecoration': 'underline'})
            ], className="mb-3"),

            dbc.Row([
                html.Div(className="text-primary text-center fs-3", id='publication-count')
            ], className="mb-3"),         
        ], style={
            "margin-left": "10px",
            "border": "2px solid #007BFF",
            "border-radius": "10px",
            "padding": "10px"
        }, width=6),

        # widget 6: faculty profile page. It displays their photo, name, email, and phone. 
        dbc.Col([
            dbc.Row([
                html.Div('Faculty Profiile', className="text-primary text-center fs-3 mb-3 mt-3"),
                html.Img(id='faculty-photo', width=150, height=250),
                html.Div('Name:', className="text-primary text-center fs-5 mb-3 mt-3"),
                html.Div(className="text-primary text-center fs-5", id='faculty-name'), 
                html.Div('Position:', className="text-primary text-center fs-5 mb-3 mt-3"),
                html.Div(className="text-primary text-center fs-5", id='faculty-position'),
                html.Div('Email:', className="text-primary text-center fs-5 mb-3 mt-3"),
                html.Div(className="text-primary text-center fs-5", id='faculty-email'),
                html.Div('Phone:', className="text-primary text-center fs-5 mb-3 mt-3"),
                html.Div(className="text-primary text-center fs-5", id='faculty-phone')
            ])
        ], style={
            "margin-left": "10px",
            "border": "2px solid #007BFF",
            "border-radius": "10px",
            "padding": "10px"
        }, width=2)
    ], className="mb-3")
], fluid=True)

# widget 1
@callback(
    Output(component_id='faculty-count', component_property='children'),
    Input(component_id='university-dropdown', component_property='value'),
)
def update_faculty_count(uni_id):
    return mysql.faculty_count(uni_id)

# widget 2
@callback(
    Output(component_id='faculty-table', component_property='data'),
    Input(component_id='university-dropdown', component_property='value'),
)
def update_faculty_table(uni_id):
    data = mysql.faculty_table(uni_id)
    return data

#widget 3
@callback(
    Output(component_id="graph", component_property="figure"),
    Input(component_id="university-dropdown", component_property="value")
)
def generate_chart(uni_id):
    df = px.data.tips()
    data = mysql.keyword_bar_chart(uni_id)
    names = []
    values = []

    for i in data:
        names.append(i[0])

    for i in data:
        values.append(i[1])

    fig = px.bar(df, x=values, y=names,
        labels={
            "x": "Count",
            "y": "Keywords"
        })
    return fig
# widget 4  
@callback(
    Output(component_id='faculty-dropdown', component_property='options'),
    Input(component_id='university-dropdown', component_property='value'),
)
def update_faculty_dropdown(uni_id):
    data = mysql.faculty_dropdown(uni_id)
    return data

@callback(
    Output(component_id='keyword-list', component_property='children'),
    Output(component_id='publication-count', component_property='children'),
    Input(component_id='university-dropdown', component_property='value'),
    Input(component_id='faculty-dropdown', component_property='value')
)
def update_keyword(uni_id, name):
    keyword_data = mongodb.get_keywords(uni_id, name)
    publication_data = neo4j.get_publication_count(name)
    return keyword_data, publication_data

# widget 5
@callback(
    Output(component_id='form-submitted', component_property='children'),
    Output(component_id='name-input', component_property='value'),
    Output(component_id='position-input', component_property='value'),
    Output(component_id='email-input', component_property='value'),
    Output(component_id='phone-input', component_property='value'),
    Output(component_id='university-input', component_property='value'),
    Input(component_id='submit-button', component_property='n_clicks'),
    [State('name-input', 'value'),
     State('position-input', 'value'),
     State('email-input', 'value'),
     State('phone-input', 'value'),
     State('university-input', 'value')]
)
def insert_into_faculty(n_clicks, name, position, email, phone, uni_affiliation):
    if n_clicks is None:
        raise PreventUpdate
    
    if not all([name, position, email, phone, uni_affiliation]):
        return html.Div("Please fill out all required fields"), name, position, email, phone, uni_affiliation

    try:
        mysql.insert_faculty(name, position, email, phone, uni_affiliation)
    except Exception as e:
        error_message = traceback.format_exc()
        print(error_message)
        return html.Div("Error insterting data: " + str(Exception)), name, position, email, phone, uni_affiliation

    return html.Div("Faculty Inserted!"), '', '', '', '', ''

# widget 6
@callback(
    Output(component_id='faculty-photo', component_property='src'),
    Output(component_id='faculty-name', component_property='children'),
    Output(component_id='faculty-position', component_property='children'),
    Output(component_id='faculty-email', component_property='children'),
    Output(component_id='faculty-phone', component_property='children'),
    Input(component_id='faculty-dropdown', component_property='value')
)
def update_faculty_profile(name):
    data = mysql.get_faculty_profile(name)
    photo = ""
    faculty_name = ""
    position = ""
    email = ""
    phone = ""
    if data != []:
        photo = data[0].get('Photo')
        faculty_name = data[0].get('Name')
        position = data[0].get('Position')
        email = data[0].get('Email')
        phone = data[0].get('Phone')
    return photo, faculty_name, position, email, phone

if __name__ == '__main__':
    app.run(debug=True)