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

app = dash.Dash()
numeric_fields = ['LotFrontage','LotArea', 'OverallQual' ,'OverallCond']
categorical_fields = {
    'MSZoning': [ 'A', 'C', 'FV','I','RH', 'RL','RP', 'RM'],
    'Street' : ['Grvl',	'Pave'] ,
    'Alley' : [ 'Grvl', 'Pave','NA' ],
    'LotShape' : ['Reg'	,'IR1', 'IR2', 'IR3']
}


app.layout = html.Div( [
    html.Div(
    [dcc.Input(id ="{}_id".format(field), value=0, type= 'number',placeholder="input {}".format(field) ) for field in numeric_fields] 
    ),

    html.Br(),

    html.Div(
        [
        dcc.Input(id ="MSZoning_id", list="MSZoning_list", value='', type= 'text',placeholder="input {}".format('MSZoning')),
        dcc.Input(id ="Street_id", list="Street_list", value='', type= 'text',placeholder="input {}".format('Street')),
        dcc.Input(id ="Alley_id", list="Alley_list", value='', type= 'text',placeholder="input {}".format('Alley')),
        dcc.Input(id ="LotShape_id", list="LotShape_list", value='', type= 'text',placeholder="input {}".format('LotShape')),
       
        html.Datalist(id="MSZoning_list", children=[
        html.Option(value=field) for field in categorical_fields['MSZoning']
            ]),

        html.Datalist(id="Street_list", children=[
        html.Option(value=field) for field in categorical_fields['Street']
            ]),

        html.Datalist(id="Alley_list", children=[
        html.Option(value=field) for field in categorical_fields['Alley']
            ]),

        html.Datalist(id="LotShape_list", children=[
        html.Option(value=field) for field in categorical_fields['LotShape']
            ]),
        html.Br(),
        html.Div(id="out-all-types")


        ]),
        html.Br(),
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Br(),
        html.Div(id='price')  
])


@app.callback(Output("price", "children"),
    [Input('submit-val', 'n_clicks')],
    [State("{}_id".format(field), 'value') for field in numeric_fields + list(categorical_fields.keys())]
    )
def submit(n_clicks, *vals):
    clmn =  numeric_fields + list(categorical_fields.keys())
    df = pd.DataFrame({clmn[v] : [vals[v]] for v in range(len(vals))})
    return str(pipe.predict(df))
    
if __name__ == '__main__':
    app.run_server(debug=True)