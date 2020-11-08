from flask import Flask,render_template
from handler import scrape_handler
import pymongo

# create instance of Flask app
# app = Flask(__name__)
app=Flask(__name__,template_folder='templates')



conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.scrape_db



# create route that renders index.html template
@app.route("/scrape")
def scrape():
    # IMPORTANT: Flask expects us to adhere to a particular folder structure.
    # It expects that all html pages will be held in the `templates` directory.
    # Because of this, we don't need to pass a relative path to the html page. It automatically
    # assumes that it's in the templates directory.
    ##    return render_template("index.html", CHRIS_TEST="HELLO WORLD!!")
    
    scrape_handler()
    mars_data = db.mars.find()[0]
    return render_template("./index.html", render_data=mars_data)

@app.route("/")
def index():
    # IMPORTANT: Flask expects us to adhere to a particular folder structure.
    # It expects that all html pages will be held in the `templates` directory.
    # Because of this, we don't need to pass a relative path to the html page. It automatically
    # assumes that it's in the templates directory.
    mars_data = db.mars.find()[0]
    return render_template("./index.html", render_data=mars_data)

if __name__ == "__main__":
    app.run(debug=True)


