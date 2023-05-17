from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

from mongo import mymongo
from scraper.scrap import scraping


app= Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/scrap',methods=['POST','GET']) # route with allowed methods as POST and GET
def index():
    if request.method == 'POST':
        # random_input = request.form['content'].replace(" ","") # obtaining the search string entered in the form

        try:
            obj2 = scraping()
            obj2.course_scrap()
            obj2.insert_Courses("iNeuron", "allcourses")
            return render_template('result.html',ineuron_data=obj2.new_list)

       
        except:
            return 'something is wrong'
            # return render_template('results.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    # app.run(port=8000,debug=True)
    app.run()






