#-----------------ライブラリのインポート-------------------
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go

import os
import datetime as dt

import time
import datetime
import pickle

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
#-----------------ライブラリのインポート----終了---------------

#-----------------@callback以下で使う関数を定義--------------------
#文字列を日付時間に変換
def to_dateAndTime(date):
    t = dt.datetime.strptime(date, '%Y%m%d%H%M')
    return t

def to_dateOnly(date):
    
    t = dt.datetime.strptime(date, '%Y%m%d')
    return t
#-----------------@callback以下で使う関数を定義----終了----------------


selectMesh = [533936904, 533936913, 533936914, 533936923, 533946002, 533946004, 533946011, 533946012, 
              533946013, 533946014, 533946021, 533946023, 533946102, 533946111, 533946112, 533946121]
slectGenderAge = ['male15', 'male20', 'male30', 'male40', 'male50', 'male60', 'male70', 
                   'female15', 'female20', 'female30', 'female40', 'female50', 'female60', 'female70']
# vars_cat = [var for var in df.columns if var.startswith('cat')]
# vars_cont = [var for var in df.columns if var.startswith('cont')]

                                                          
                                                                   
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
server = app.server   

#-----------------画面左側パラメータ設定部分-------------------------------------
sidebar = html.Div(
    [
        dbc.Row(
            [
                html.H5('Settings',
                        style={'margin-top': '14px', 'margin-left': '3vh'})
                ],
            style={"height": "5vh"},
            className='bg-primary text-white font-italic'
            ),
        dbc.Row(
            [
                html.Div([
                    html.P('Select_Indicate_Date',
                           style={'margin-top': '1vh', 'margin-bottom': '1vh'},
                           className='font-weight-bold'),
                    dcc.Input(id='input_date_form', value='Write_Date_wiht_YYYYMMDD',
                                 style={'width': '20vh'}
                                 ),
                    html.P('Select_Indicate_MeshCode',
                           style={'margin-top': '3vh', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='selected_mesh', multi=True, 
                                 value=selectMesh,
                                 options=[{'label': x, 'value': x}
                                          for x in selectMesh],
                                 style={'width': '20vh'}
                                 ),
                    html.P('Select_Indicate_Attribute',
                           style={'margin-top': '16px', 'margin-bottom': '1vh'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='selected_attribute', multi=True,
                                 value=slectGenderAge,
                                 options=[{'label': x, 'value': x}
                                          for x in slectGenderAge],
                                 style={'width': '20vh'}
                                 ),
                    html.Button(id='Button_Run', n_clicks=0, children='Run',
                                style={'margin-top': '3vh'},
                                className='bg-dark text-white')
                ]
                )
            ],
            style={'height': '95vh', 'margin': '2vh'})
        ]
    )
#-----------------画面左側パラメータ設定部分----終了-----------------------------

#-----------------画面右側グラフ描画部分-----------------------------------------
content = html.Div(
    [
                
                dbc.Col(
                    [
                        html.Div([
                            html.P('Map MeshCode',
                                   className='font-weight-bold'),
                            dcc.Graph(id='graph_m',className='bg-light'),
                        ])]),
                dbc.Col(
                    [
                        html.Div([
                            html.P('Mobile Spatial Statistics',
                                   className='font-weight-bold'),
                            dcc.Graph(id='graph',className='bg-light')])
                        ]) ])
                                               
        
 
                
#-----------------画面右側グラフ描画部分----終了---------------------------------

#-----------------何してるかわからないが消すとエラー吐く--------------------------
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='bg-light'),
                dbc.Col(content, width=9)
                ]
            )
        ],
    fluid=True
    )
#-----------------何してるかわからないが消すとエラー吐く----終了------------------

#-----------------@callback以下でインタラクティブな処理を実現----------------------
@app.callback(
    Output("graph_m", "figure"),
    Input("Button_Run", "value"))

###メッシュのマップを作製
def createMeshMap(date):
    gdf=gpd.read_file('data/MESH05339.shp')
    mesh_list = [533936904, 533936913, 533936914, 533936923, 533946002, 533946004, 533946011, 533946012, 533946013, 533946014, 533946021, 533946023, 533946102, 533946111, 533946112, 533946121]
    b = []
    for k in mesh_list:
        a =gdf[gdf['KEY_CODE'] == str(k)]
        b.append(a)
    gdf_target = pd.concat(b)

    gdf_p = gpd.read_file('data/銀座さとう/肉屋さとう.shp')

    px.set_mapbox_access_token('pk.eyJ1IjoidG9yYWppIiwiYSI6ImNsMmEzb25lMzAxbnEzZHFkMW0yd2R0MXcifQ.qmBfWxGD1UPg8NKAeA6bMg')
    figm = px.choropleth_mapbox(gdf_target, geojson=gdf_target.geometry, 
                               locations=gdf_target.index,
                               color='KEY_CODE',
                               color_continuous_scale="Viridis",
                               mapbox_style="carto-positron",
                               zoom=15, 
                               center={'lat':35.67424959466421, 'lon':139.76981553072267},
                               opacity=0.4
                               #labels={'unemp':'unemployment rate'}
                              )
    figm.add_scattermapbox(
        lat = [35.67341],
        lon = [139.76973] ,
        mode = 'markers+text',
        text= '銀座さとう',
        marker_size=12,
        marker_color='rgb(235, 0, 100)'
    )
    figm.update_layout(mapbox_style='carto-positron')
    figm.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return figm

@app.callback(
    Output("graph", "figure"), 
    Input("input_date_form", "value"),
    Input("selected_mesh", "value"),
    Input("selected_attribute", "value"))
###選択されたメッシュと属性を可視化する。
def analysis(date,mesh,attribute):
    
    #input 異なる日にちで比較するか選択してもらう
    #which = 0 # 0 or 1   0:同じ日付内で比較します。　1:異なる日付で比較します。
    whici = 0

    if which == 0:
        ##選択された要素のみDataFrameから抽出
        slectGenderAge = attribute
        selectDate = int(date)
        selectMonth = str(selectDate)[0:6]
        selectMesh = mesh
        #[533936904, 533936913, 533936914, 533936923, 533946002, 533946004, 533946011, 533946012, 533946013, 533946014, 533946021, 533946023, 533946102, 533946111, 533946112, 533946121]

        #指定されたMonthとMeshのpklファイルのpathを取得
        df_rn_list = []
        for num, p in enumerate(selectMesh):
            path = 'forApp/' + str(p) + '/' + selectMonth + '.pkl'

            #指定されたDateをint→datetimeへ
            date = to_dateOnly(str(selectDate))
            date_s = date - datetime.timedelta(hours=1)#選択したdateの24時間分のデータを取得するために前日の1時間前を指定
            date_g = date + datetime.timedelta(days=1)

            #指定された日のdataframe生成
            df_from_pkl = pd.read_pickle(path)
            df_target_mesh_date = df_from_pkl[((df_from_pkl['date'] > date_s) & (df_from_pkl['date'] < date_g))]

            #slectGenderAgeに複数渡される場合に備えてitemに渡すリストを作成
            slectGenderAge.insert(0,'date')
            df_target_narrowed = df_target_mesh_date.filter(items=slectGenderAge)

            #columnの書き換え（異なるMeshで比較を行う場合に備えて、columnにメッシュコードを付与する。）
            column_list = list(df_target_narrowed.columns)
            n_column_list = []
            for k in column_list:
                if k == 'date':
                    n = k
                else:
                    n = k + '_' + str(p)

                n_column_list.append(n)

            forRename = dict(zip(column_list,n_column_list))
            df_target_narrowed_rn = df_target_narrowed.rename(columns=forRename)

            if num == 0:
                pass
            else:
                df_target_narrowed_rn = df_target_narrowed_rn.drop(columns=['date'])



            df_rn_list.append(df_target_narrowed_rn)

        df_target_result = pd.concat(df_rn_list, axis=1)
    else:
        print("異なる日付を比較する機能はまだ未完成です。。。")
        
    data = []
    for col in df_target_result.columns[1:]:
        if col != 'date':
            data.append(go.Scatter(x=df_target_result['date'],
                                  y=df_target_result[col],
                                  name=col))              
    fig_res = go.Figure(data)

    return fig_res
#-----------------@callback以下でインタラクティブな処理を実現----終了------------------


#-----------------アプリを実行--------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
    #app.run_server(mode="inline")
#-----------------アプリを実行----終了------------------