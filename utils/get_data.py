from jugaad_data.nse import stock_df, NSELive
import pandas as pd
from datetime import date, datetime
import matplotlib.pyplot as plt
import plotly.express as px

def get_stock_data(stock_symbol, start_date, end_date, criteria):
    criteria = criteria.upper()
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()    
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

# def generate_combined_graph(criteria, stock_symbols,start_date,end_date):
#     dataframes=[]
#     criteria = criteria.upper()
#     start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#     end_date = datetime.strptime(end_date, "%Y-%m-%d").date()  
#     for stock_symbol in stock_symbols:
#         df = stock_df(symbol=stock_symbol, from_date=start_date, to_date=end_date, series="EQ")
#         dataframes.append(df)

    
#     fig = px.line(title=f"{criteria} vs Date for Multiple Stocks")

    
#     for df, stock_symbol in zip(dataframes, stock_symbols):
#         df_subset = df[["DATE", criteria]]
#         fig.add_trace(px.line(df_subset, x="DATE", y=criteria, name=stock_symbol).data[0])

    
#     filepath = f"static/graph/combined_{criteria}.html"

#     fig.write_html(filepath)
#     return filepath
def generate_combined_graph(criteria, stock_symbols, start_date, end_date):
    criteria = criteria.upper()
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()  

    
    dataframes = [stock_df(symbol=stock_symbol, from_date=start_date, to_date=end_date, series="EQ") for stock_symbol in stock_symbols]
    fig = px.line(title=f"{criteria} vs Date for Multiple Stocks")

    
    for df, stock_symbol in zip(dataframes, stock_symbols):
        df_subset = df[["DATE", criteria]]
        fig.add_trace(px.line(df_subset, x="DATE", y=criteria, name=stock_symbol))

    filepath = f"static/graph/combined_{criteria}.html"

    fig.write_html(filepath)
    return filepath