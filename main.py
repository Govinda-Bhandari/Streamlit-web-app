'''Importing required Data Sets'''
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

#Page Configuaration
st.set_page_config(
    page_title="Web App Project by Govinda Bhandari" ,
    layout="wide" ,
    initial_sidebar_state="expanded") # page layout and sidebar size

    #Creating Web App Windows
def main(): # function to run whole code
    menu_item = ("Home", "Candlestick Chart", "Cumulative Return") # To display window according to users menu item choice,
    choice = st.sidebar.selectbox("Project Content Menu" , menu_item)
    if choice == 'Home': # if choice is Home from menu
        st.subheader('Home') # Creating Homepage window
        with st.container():
            col1 , col2 = st.columns((2, 1)) # showing in column to appear data in given column order
            with col1:
                st.markdown( # to use html tag and css style property
                    "<h2 style='text-align: center; color: White;'><b>Uniwersytet Marii Curie-Skłodowskiej,Lublin.</b></h2>"
                    , unsafe_allow_html=True)
            with col2:
                st.image('umcs.png' , width=200)

            st.markdown(
                "<h3 style='text-align: center; color: White;'><i>Programming for Data Science final project.</i></h3>" # applying html and css property to the text
                , unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; color: #FF4B4B;'><i>Prepared by : Govinda Bhandari.</i></h4>"
                        , unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; color: #FF4B4B;'><i>Student id : 310907.</i></h4>"
                        , unsafe_allow_html=True)
        with st.container(): # Dataset in a form of table and short description container
            st.write('---')
            st.subheader('Information about Data')
            st.write(
                'Data is imported by using Yahoo finance python library.Datasets are from WIG20 index listed companies stock data from Warsaw Stock Exchange.')
            st.write('---')

            #Acessing Data from WIG20 list using from Yahoo Finance website using yfinance python library.
            WIG20 = ('ING.WA' , 'PZU.WA' , 'SPL.WA' , 'ALE.WA' , 'CDR.WA' , 'PEO.WA' , 'MRC.WA' , 'PGE.WA' , 'PKN.WA') # stock symbol
            stock_symbol = st.selectbox('Choose your stock' , WIG20)
            Start = st.date_input('Start_Date' , value=pd.to_datetime('2018-01-02')) # stock date strated from 2018
            Upto = st.date_input('End_Date' , value=pd.to_datetime('today')) # Stock date till last trading session also user can select previous range

        def load_data(symbol):
            if len(symbol) > 0: # checking list for stocks symbol by using len function
                df = yf.download(symbol , Start , Upto)
                df.reset_index(inplace=True) # resetting datasets index
                if symbol == 'ING.WA': # checking if the symbol is match with condition to display short information about symbol stock company.
                    st.write('You have selected, ING bank stock data.', format(symbol))
                elif symbol == 'PZU.WA':
                    st.write('You have selected, PZU insurance company stock data.', format(symbol))
                elif symbol == 'SPL.WA':
                    st.write('You have selected, Santander Bank stock data.', format(symbol))
                elif symbol == 'ALE.WA':
                    st.write('You have selected, Allegro online store stock data.', format(symbol))
                elif symbol == 'CDR.WA':
                    st.write('You have selected, CD PROJECT RED gaming company stock data.', format(symbol))
                elif symbol == 'PEO.WA':
                    st.write('You have selected, PEKAO bank stock data.', format(symbol))
                elif symbol == 'MRC.WA':
                    st.write('You have selected, MERCATOR MEDICAL company stock data.', format(symbol))
                elif symbol == 'PGE.WA':
                    st.write('You have selected, Polish Energy Group company stock data.', format(symbol))
                else:
                    st.write('You have selected, Orlen fuel company stock data.', format(symbol))
                st.write(df.tail())

        load_data(stock_symbol)

        #Candle Stick Chart Window
    if choice == 'Candlestick Chart': #Condition if user select Candlestick Chart
        st.subheader('Candle stick chart')
        WIG20 = ('','ING.WA', 'PZU.WA', 'SPL.WA', 'ALE.WA', 'CDR.WA', 'PZU.WA', 'PEO.WA', 'MRC.WA', 'PGE.WA', 'PKN.WA')
        stock_symbol = st.selectbox('Choose your stock', WIG20)
        Start = st.date_input('Start_Date', value=pd.to_datetime('2021-11-02'))
        Upto = st.date_input('End_Date', value=pd.to_datetime('today'))
        def create_chart(symbol):
            if len(symbol) > 0:
                df = yf.download(symbol, Start, Upto)
                df.reset_index(inplace=True)

                fig = go.Figure(data=[go.Candlestick(x=df['Date'], # Candlestick chart plot using plotly
                                                     open=df['Open'],
                                                     high=df['High'],
                                                     low=df['Low'],
                                                     close=df['Adj Close'])])
                fig.update_layout(xaxis_rangeslider_visible=True,title = (f'Candle stick chart for {format(symbol)}. (Hover over the candlestick in chart  to see data each candlestick contains)'),template = 'plotly_dark')
                fig.update_xaxes(title = 'Date range slider')
                fig.update_yaxes(title = 'Price range in (Złoty) ')
                fig.show()
        create_chart(stock_symbol)
    # Cumulative return window
    if choice == 'Cumulative Return':
        st.subheader('Return')
        st.markdown("<h1 style='text-align: center; color: white;'>Cumulative return and stock return comparison</h1>", unsafe_allow_html=True)
        WIG20 = ('ING.WA', 'PZU.WA', 'SPL.WA', 'ALE.WA', 'CDR.WA', 'PZU.WA', 'PEO.WA', 'MRC.WA', 'PGE.WA', 'PKN.WA')
        stock_symbol = st.multiselect('Choose your stock or choose multiple stock to compare' , WIG20)
        Start = st.date_input('Start_Date', value=pd.to_datetime('2018-01-01'))
        Upto = st.date_input('End_Date', value=pd.to_datetime('today'))

        def stock_return(df):
            returns = df.pct_change() # assigning returns value as a percentage change from datasets
            cumulative_return = (1 + returns).cumprod() - 1 # formula to calculate cumulative return
            cumulative_return = cumulative_return.fillna(0)
            return cumulative_return

        def return_compare(symbol):
            if len(symbol) > 0:
                df = stock_return(yf.download(symbol , Start , Upto)['Adj Close']) # by using stock_return functions datasets wll bedownload and converted as a formula
                st.write('Cumulative Return for' , format(symbol))
                st.line_chart(df) # making chrat using line_chart function
        return_compare(stock_symbol)

if __name__ == '__main__':
    main() # main function for all code.
