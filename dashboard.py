import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import joblib
import numpy as np
import pandas as pd
from custom_preprocessor import custom_preprocessor
from ModifiedLabelEncoder import ModifiedLabelEncoder
pipe = joblib.load('pipe.joblib')

app = dash.Dash(title= 'House Pricing')

numeric_fields = ['LotFrontage','LotArea', 'OverallQual' ,'OverallCond',
 'YearBuilt', 'YearRemodAdd','MSSubClass', 'TotalBsmtSF','GrLivArea', 'BsmtFullBath']
categorical_fields = ['MSZoning', 'Street','Alley' ,'LotShape' ]
style = {
        'height': '25px',
        'width':'200px',
        'margin-top': '10px',
        'margin-bottom': '10px',
        'margin-right': '10px',
        'margin-left': '0px',
       }

style_numeric = {
        'height': '25px',
        'width':'50px',
        'margin-top': '10px',
        'margin-bottom': '10px',
        'margin-right': '10px',
        'margin-left': '5px',
       }


app.layout = html.Div( [

     html.Div([html.Label([field,
         dcc.Input(id ="{}_id".format(field), value=0, type= 'number',placeholder="input {}".format(field),  style=style_numeric ) 
     ]) for field in numeric_fields]),
     html.Br(),
     html.Label(["zoning classification", dcc.Dropdown(id="MSZoning_id", options = [
         {'label':'Agriculture', 'value':'A'},
         {'label':'Commercial', 'value':'C'},
         {'label':'Floating Village Residential', 'value':'FV'},
         {'label':'Industrial', 'value':'I'}
     ], value='A' , style=style
      )]),

    html.Br(),
     html.Label(["street access", dcc.Dropdown(id="Street_id", options = [
         {'label':'Gravel', 'value':'Grvl'},
         {'label':'Paved', 'value':'Pave'}
     ], value='Grvl',style=style)]),

    html.Br(),
    html.Label(["alley access", dcc.Dropdown(id="Alley_id", options = [
         {'label':'Gravel', 'value':'Grvl'},
         {'label':'Paved', 'value':'Pave'},
         {'label':'No alley', 'value':'NA'}
     ], value='Grvl',style=style)]),

    html.Br(),
    html.Label(["shape of property", dcc.Dropdown(id="LotShape_id", options = [
         {'label':'Regular', 'value':'Reg'},
         {'label':'Slightly irregular', 'value':'IR2'},
         {'label':'Moderately Irregular', 'value':'IR3'},
         {'label':'Irregular', 'value':'Regular'}
     ], value='Reg',style=style)]),

    html.Br(),
    html.Button('Submit', id='submit-val', n_clicks=0, style= {'background-color':'MediumSeaGreen'}),
    html.Br(),
    html.Div(id='price')  
])


@app.callback(Output("price", "children"),
    [Input('submit-val', 'n_clicks')],
    [State("{}_id".format(field), 'value') for field in numeric_fields + categorical_fields]
    )
def submit(n_clicks, *vals):
    clmn =  numeric_fields + categorical_fields
    df = pd.DataFrame({clmn[v] : [vals[v]] for v in range(len(vals))})
    price = pipe.predict(df)[0]
    return "Price: {}".format(str(price))
    
if __name__ == '__main__':
    app.run_server(debug=True)