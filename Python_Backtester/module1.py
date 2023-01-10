import pandas as pd

#FYI: Must manually copy excel file from algo source files to backtester source files
excel_df=pd.read_csv('apple_contract.csv')





def test(): 
    buy = -2
    data = []
    for index, row in excel_df.iterrows():
        if (row['Close'] < row['VWAP']) and (buy == 1):
            buy = -1
            print('Sell')
            print(row['DateTime'])
            data.append['Time'] = row['DateTime']
            data.append['Order'] = 'sell'
        else: 
            if (row['Close'] > row['VWAP']) and (buy == 0):
                buy = 1
                print('Buy')
                print(row['DateTime'])
                data.append['Time'] = row['DateTime']
                data.append['Order'] = 'buy'
            else:
                if (row['Close'] > row['VWAP']) and (buy == 1):
                    buy = 1
                else:
                    buy = 0
    return data

     
test()

    
'''
df_marks = pd.DataFrame({'name': ['apple', 'banana', 'orange', 'mango'],'calories': [68, 74, 77, 78]})

for index, row in df_marks.iterrows():
    print(index, row['name'], row['calories'])
    '''




