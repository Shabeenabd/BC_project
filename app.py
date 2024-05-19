from flask import Flask, render_template, url_for, request,redirect
from model import get_responses,next_page

app = Flask(__name__)

 
#home page
@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


#result page
@app.route('/result',methods=['POST', 'GET'])
def result():
    if request.method=='POST':
        y=0
        prv=0

        #if next page button clicked then call next page function from the model file
        if request.form['x']=='Next Page':
            #to display the previous button only after initially next button clicked
            prv=1
            data=next_page()
            #if there is no next page then y is set to True and corresponding htnl elements are showed
            y=0 if data else 1
            data=data if data else 0 

        #if previous page button clicked then call previous page function from the model file
        elif request.form['x']=='Previous Page':
            data=next_page()
            y=0 if data else 1   

        #if Home page button clicked then go to the home  page
        elif request.form['x']=='Home':  
            return redirect(url_for('home'))
        else:
            #get the response-source object returned by model.py
            data=get_responses()
    return render_template('index.html', data=data,y=y,prv=prv)



if __name__ == "__main__":
    app.run(debug=True)