
from crypt import methods
from flask import Flask, render_template,request,redirect
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





@app.route('/', methods=['GET', 'POST'])
def inicio():

    if request.method == 'POST':
        score = request.form['texto_ilo']
        name = request.form['texto_hiloo']
        ranking={"name":name ,"score": score }
        dbResponse = db.ranking.insert_one(ranking)

        return redirect("http://127.0.0.1:3000/Ranking")

    return render_template("Index.html")

# @app.route('/Save',  methods=['GET', 'POST'] )
# def save():

#     score = request.form['texto_ilo']
#     name = request.form['texto_hiloo']
#     ranking={"name":name ,"score": score }
#     dbResponse = db.ranking.insert_one(ranking)

#     return redirect("http://127.0.0.1:3000/Ranking")

@app.route('/Ranking', methods=['GET', 'POST'])
def ranking():
    
    

    df= pd.DataFrame(list(collection.find()))
    df['score'] = df['score'].astype('int')
    df= df.drop(['_id'], axis=1)
    data = df.sort_values('score',ascending=False)
    data= data.head(10)
    
   

    return render_template("Ranking.html", data_rows=data.to_numpy())



if __name__ == "__main__":
    app.run(port=3000, debug=True)



 

