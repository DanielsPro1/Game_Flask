
from flask import Flask, render_template,request
import pymongo
import pandas as pd
import numpy as np



app = Flask(__name__)



# db = conf_mongo(app)
client = pymongo.MongoClient(
    host="localhost",
    port=27017,
    serverSelectionTimeoutMs= 1000
) 
db = client.game
collection = db.ranking




@app.route('/')
def inicio():

    
   
    return render_template("Index.html")


@app.route('/Ranking', methods=['GET', 'POST'])
def ranking():
    
    score = request.form['texto_ilo']
    name = request.form['texto_hiloo']
    
    ranking={"name":name ,"score": score }
    dbResponse = db.ranking.insert_one(ranking)
    df= pd.DataFrame(list(collection.find()))
    
    df['score'] = df['score'].astype('int')
    
    df= df.drop(['_id'], axis=1)
    print(df)
    
    data = df.sort_values('score',ascending=False)
    
   
    


    return render_template("Ranking.html", data_rows=data.to_numpy())

    # data_rows=data.to_numpy()



if __name__ == "__main__":
    app.run(port=3000, debug=True)



 

