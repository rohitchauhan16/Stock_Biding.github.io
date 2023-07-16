import pandas as pd
from flask import Flask, Blueprint, render_template,request,send_file, redirect, url_for, Response,session
from datetime import date, timedelta, datetime
import time
import numpy as np
import pyxlsb
import re
from flaskwebgui import FlaskUI


app = Flask(__name__)  

@app.route('/', methods = ["GET","POST"])   
@app.route('/biding', methods=['GET', 'POST'])  
def biding(): 

    if request.method == 'POST':
        cursor={} 
        cursor['Month']=request.form['MONTH']  
        cursor['ID']=request.form['ID'] 
        cursor['TYPE']=request.form['TYPE'] 
        cursor['NET_SHEET']=request.form['NET_SHEET'] 
        cursor['INTEREST']=request.form['INTEREST'] 
        cursor['TURNOVER']=request.form['TURNOVER'] 
        cursor['TOTAL_TURNOVER']=request.form['TOTAL_TURNOVER'] 
        cursor['TURNOVER_COST']=request.form['TURNOVER_COST'] 
        cursor['ID_COST']=request.form['ID_COST'] 
        cursor['PERCENTAGE']=request.form['PERCENTAGE'] 

        df =  pd.DataFrame.from_records([cursor]) 

        df['TURNOVER_CHARGES']= int(df.TURNOVER_COST) * float(df.TOTAL_TURNOVER) 
        df['TURNOVER_PROFIT']= int(df.TURNOVER) - int(df.TURNOVER_CHARGES)
        df['NET_TOTAL']=  int(df.NET_SHEET) - int(df.INTEREST) + int(df.TURNOVER_PROFIT) 
        df['AFTER_ID']= int(df.NET_TOTAL) - int(df.ID_COST)  
        df['FINAL_OUTPUT']= int(df.AFTER_ID) * float(int(df.PERCENTAGE)/ 100)    

        # df.to_csv('files/biding.csv', index=False)  
        df.to_csv('files/biding.csv', mode='a', header=False, index=False)  

        try:
            d= pd.read_csv('files/biding.csv')   
            SUM= d.FINAL_OUTPUT.sum()
        except FileNotFoundError:
            return redirect('/biding') 

        return render_template('biding.html',  
                                ID=df.ID[0], TYPE=df.TYPE[0], NET_SHEET=df.NET_SHEET[0],
                                INTEREST=df.INTEREST[0], TURNOVER=df.TURNOVER[0], TOTAL_TURNOVER=df.TOTAL_TURNOVER[0],                                          
                                TURNOVER_COST=df.TURNOVER_COST[0], ID_COST=df.ID_COST[0], PERCENTAGE=df.PERCENTAGE[0], 
                                TURNOVER_CHARGES=df.TURNOVER_CHARGES[0], 
                                TURNOVER_PROFIT=df.TURNOVER_PROFIT[0], 
                                NET_TOTAL=df.NET_TOTAL[0], 
                                AFTER_ID=df.AFTER_ID[0], 
                                FINAL_OUTPUT=str(df.FINAL_OUTPUT[0]),
                                d1=d.values, d1col= d.columns.values,   
                                SUM=str(SUM))        

    else:
        df= pd.read_csv('files/biding.csv') 
        SUM= df.FINAL_OUTPUT.sum()
        return render_template('biding.html', d1=df.values, d1col= df.columns.values, SUM=str(SUM))         
        


@app.route('/biding_export')  
def biding_export(): 
    return send_file('files/biding.csv', 
                        mimetype='text/csv',
                        attachment_filename='biding.csv',  
                        as_attachment=True)



@app.route('/ioc', methods=['GET', 'POST'])  
def ioc():  

    if request.method == 'POST':
        cursor={} 
        cursor['Month']=request.form['MONTH']  
        cursor['ID']=request.form['ID'] 
        cursor['TYPE']=request.form['TYPE'] 
        cursor['NET_SHEET']=request.form['NET_SHEET'] 
        cursor['INTEREST']=request.form['INTEREST'] 
        cursor['TURNOVER']=request.form['TURNOVER'] 
        cursor['TOTAL_TURNOVER']=request.form['TOTAL_TURNOVER'] 
        cursor['TURNOVER_COST']=request.form['TURNOVER_COST'] 
        cursor['ID_COST']=request.form['ID_COST'] 
        cursor['PERCENTAGE']=request.form['PERCENTAGE'] 

        df =  pd.DataFrame.from_records([cursor]) 

        df['TURNOVER_CHARGES']= int(df.TURNOVER_COST) * float(df.TOTAL_TURNOVER) 
        df['TURNOVER_PROFIT']= int(df.TURNOVER) - int(df.TURNOVER_CHARGES)
        df['NET_TOTAL']=  int(df.NET_SHEET) - int(df.INTEREST) + int(df.TURNOVER_PROFIT) 
        df['AFTER_ID']= int(df.NET_TOTAL) - int(df.ID_COST)  
        df['FINAL_OUTPUT']= int(df.AFTER_ID) * float(int(df.PERCENTAGE)/ 100)    

        # df.to_csv('files/ioc.csv', index=False)  
        df.to_csv('files/ioc.csv', mode='a', header=False, index=False)  
        try:

            d= pd.read_csv('files/ioc.csv')   
            SUM= d.FINAL_OUTPUT.sum()

        except FileNotFoundError:
            return redirect('/ioc') 

        return render_template('ioc.html',  
                                ID=df.ID[0], TYPE=df.TYPE[0], NET_SHEET=df.NET_SHEET[0],
                                INTEREST=df.INTEREST[0], TURNOVER=df.TURNOVER[0], TOTAL_TURNOVER=df.TOTAL_TURNOVER[0],                                          
                                TURNOVER_COST=df.TURNOVER_COST[0], ID_COST=df.ID_COST[0], PERCENTAGE=df.PERCENTAGE[0], 
                                TURNOVER_CHARGES=df.TURNOVER_CHARGES[0], 
                                TURNOVER_PROFIT=df.TURNOVER_PROFIT[0], 
                                NET_TOTAL=df.NET_TOTAL[0], 
                                AFTER_ID=df.AFTER_ID[0], 
                                FINAL_OUTPUT=str(df.FINAL_OUTPUT[0]),
                                d1=d.values, d1col= d.columns.values,   
                                SUM=str(SUM))       

    else:
        df= pd.read_csv('files/ioc.csv')   
        SUM= df.FINAL_OUTPUT.sum()
        return render_template('ioc.html', d1=df.values, d1col= df.columns.values, SUM=str(SUM))         
        

    

@app.route('/ioc_export')  
def ioc_export():
    return send_file('files/ioc.csv', 
                        mimetype='text/csv',
                        attachment_filename='ioc.csv',  
                        as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)  
    # FlaskUI(app=app, width=1200, height=800).run()  

    