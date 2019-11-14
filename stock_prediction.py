import numpy as np
from sklearn.linear_model import LinearRegression
from pandas_datareader import data as dt
import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
import datetime
def fun(stock,test,days,lab,message):
    global f
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime.now()
    f = dt.DataReader(stock, 'tiingo', start, end,access_key='911ee28d70118f9cea5a84d2b8f1436fa32d3116')
    f.reset_index(inplace=True)
    f.set_index('date',inplace=True)
    f=f[['adjClose', 'adjHigh', 'adjLow', 'adjOpen', 'adjVolume',]]
    no_days=int(days)
    f['newclose']=f['adjClose'].shift(-no_days)
    x=f.drop(['adjClose','newclose'],axis=1)
    y=f['newclose'].dropna()
    x1=x[:-no_days]
    x_pr=x[-no_days:]
    x_tr,x_ts,y_tr,y_ts=train_test_split(x1,y,test_size=float(test))
    alg=LinearRegression()
    alg.fit(x_tr,y_tr)
    lab.config(text=str(alg.score(x_ts,y_ts)))
    prd=alg.predict(x_pr)
    message.config(text=str(prd))
    lastday=f.iloc[-1].name
    f['forecast']=np.nan
    for i in prd:
        lastday+=datetime.timedelta(1)
        f.loc[lastday]=[np.nan for _ in range(6)]+[i]
def vis():
    %matplotlib tk
    f['adjClose'].plot()
    f['forecast'].plot()
    plt.show()

from tkinter import *
def gui():
    scr=Tk()
    label=Label(scr,font=('times',20,'bold'),text='stock name')
    label.grid(row=0,column=0)
    stock=StringVar()
    op=OptionMenu(scr,stock,'tcs','aple','googl','msft')
    op.grid(row=0,column=1)
    label1=Label(scr,font=('times',20,'bold'),text='test Size')
    label1.grid(row=1,column=0)
    test=DoubleVar()
    op1=OptionMenu(scr,test,0.1,0.2,0.3)
    op1.grid(row=1,column=1)
    label2=Label(scr,font=('times',20,'bold'),text='number of days')
    label2.grid(row=2,column=0)
    e=Entry(scr,font=('times',20,'bold'))
    e.grid(row=2,column=1)
    b=Button(scr,text='evaluate',font=('times',20,'bold'),command=lambda :fun(stock.get(),test.get(),e.get(),label4,m))
    b.grid(row=3,column=0)
    b1=Button(scr,text='visualize',font=('times',20,'bold'),command=vis)
    b1.grid(row=3,column=1)
    label3=Label(scr,font=('times',20,'bold'),text='Acurracy')
    label3.grid(row=4,column=0)
    label4=Label(scr,font=('times',20,'bold'))
    label4.grid(row=4,column=1)
    m=Message(scr,font=('times',20,'bold'))
    m.grid(row=5,columnspan=7)
    scr.mainloop()
gui()
