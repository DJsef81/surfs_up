# This dependency will enable your code to access all that Flask has to offer.
# To import the Flask dependency, add the following to your code:

from flask import Flask


# Create a New Flask App Instance
# "Instance" is a general term in programming to refer to a singular version of something. 
# Add the following to your code to create a new Flask instance called app:

app = Flask(__name__)

# Create Flask Routes
# First, we need to define the starting point, also known as the root. 

@app.route('/')
def hello_world():
    return 'Hello world'