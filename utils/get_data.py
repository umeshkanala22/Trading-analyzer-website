from jugaad_data.nse import stock_df, NSELive
import pandas as pd
from datetime import date, datetime
import matplotlib.pyplot as plt
import plotly.express as px

def get_stock_data(stock_symbol, start_date, end_date, criteria):
    
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()    
    print(start_date, end_date)
    df = stock_df(symbol=stock_symbol, from_date=start_date, to_date=end_date, series="EQ")
    df = df[["DATE", "OPEN", "CLOSE", "HIGH", "LOW", "LTP", "VOLUME", "VALUE", "NO OF TRADES"]]
    graph_image = generate_graph(df, criteria, stock_symbol)
    return graph_image

def get_live_stock_data(stock_symbol):
    n = NSELive()
    data = n.stock_quote(stock_symbol)
    return data['priceInfo']    

def generate_graph(df, criteria, stock_symbol):
    df = df[["DATE", criteria]]
    fig = px.line(df, x="DATE", y=criteria, title=criteria + " vs Date for " + stock_symbol)
    filepath = "static/graph/" + stock_symbol + "_" + criteria + ".html"
    fig.write_html(filepath)
    return filepath