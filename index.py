from flask import Flask, render_template
from flask import request
import pandas as pd
app = Flask(__name__)
#app = Flask(__name__, template_folder='template')  

@app.route("/")




#deposit=10
# threshold=0.25


    
def index():
    final_matrix=pd.read_csv("https://www.dropbox.com/s/g21186mjf80hy0n/final_matrix_parquet.csv?dl=1")
    #final_matrix=final_matrix.set_index('Range_of_Balance').iloc[1:,:]

    threshold = request.args.get("threshold", "")
    deposit = request.args.get("deposit", "")
    #deposit=10
    if threshold:
        fahrenheit = combinations(float(threshold),float(deposit))
    else:
        fahrenheit = ""
    return (
        """<form action="" method="get">
         threshold: <input type="text" name="threshold">
                Deposit: <input type="text" name="deposit">
                <input type="submit" value="Get the Deposit">
            </form>"""
        
        
        + "Deposit: " + deposit
        + "threshold: " + threshold
        
        + fahrenheit
    )
    
    
    
    

def get_df(threshold):
    final_matrix=pd.read_csv("https://www.dropbox.com/s/g21186mjf80hy0n/final_matrix_parquet.csv?dl=1")
    #final_matrix=final_matrix.set_index('Range_of_Balance').iloc[1:,:]
    look_for_value=final_matrix.iloc[1:,2:61]
    my_df_values=look_for_value[look_for_value<=threshold]
    range_balance_df=final_matrix[['all_balance_x','all_balance_y']].rename(columns={'all_balance_x':'the_min','all_balance_y':'the_max'})
    my_df_values=my_df_values.merge(range_balance_df,left_index=True,right_index=True)
    return my_df_values

def get_bonus(dep,ratio):
    bonus_to_give = (dep*ratio)/(30-ratio)
    final_balance=dep+bonus_to_give
    return final_balance,bonus_to_give

def get_balance_range(threshold,balance):
    my_df_values = get_df(threshold) 
    #the_row=my_df_values[(my_df_values['the_min']>=balance)].iloc[0,:].name
    the_row=my_df_values[(my_df_values['the_min']<=balance)&(my_df_values['the_max']>=balance)].iloc[0,:].name
    return the_row

def validate_percentage(balance,ratio,threshold):
    my_df_values = get_df(threshold)
    the_index=get_balance_range(threshold,balance)
    if my_df_values.loc[the_index,ratio]<=threshold:
        return 'True'
    else:
        return 'False' 

def look_in_DF(df,threshold,deposit):
    the_list=[]
    df=df[df['the_min']>deposit]
    for i in df.index:
        for j in df.columns:
            if df.loc[i,j]<threshold:
                balance,bonus=get_bonus(deposit,float(j))
                validate_percentage(balance,j,threshold)
                the_list.append([deposit,get_balance_range(threshold,balance),balance,bonus,float(j),validate_percentage(balance,j,threshold)])
    return the_list

def combinations(threshold,deposit):
    my_df_values = get_df(threshold) 
    the_list=look_in_DF(my_df_values,threshold,deposit)
    final_df=pd.DataFrame(the_list)
    final_df=final_df[final_df[5]!='False'].sort_values(by=4).drop_duplicates()
    final_df.rename(columns={0:'deposit',1:'balance_range',2:'new_balance',3:'bonus_to_be_awarded',4:'ratio',5:'is_true'},inplace=True)
    to_produce = final_df.iloc[:,:-1].reset_index(drop=True)
    
    #return to_produce
    return render_template('table.html', tables=[to_produce.to_html()], titles=[''])