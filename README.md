# maithuy.recommendation installation guide
1.  install python 3.6.7 and virtualev by using pip : **pip install virtualenv**
2.  Create directory for Maithuy recommendation
3.  Type in cmd: **virtualenv virtual**
4.  activate virtual environment: **.\virtual\Scripts\activate**
5.  clone project
6.  navigate to subfolder
7.  install requirement while you are in virtual env: **pip -r requirements.txt**

# maithuy.recommendation app run
***python app.py***

# maithuy.recommendation file to use
Use Buy_model xlsx file to recommend (locate at static/data)

# maithuy.recommendation metric

*  Use collaborative filtering to recommend a list of products to customer
*  Item recommendation: Display a list of 10 similar items based on 1 provided item (input 1 model number)
*  User recommendation: Display a list of 10 similar items based on list of items (input list of model number )
*  Syntax for user recommendation: list of item'numbers separeted by a space
*  For example user have buy items number 26598, 3594, 5148. So type in "26598 3594 5148"

# maithuy.recommendation future works:
*  There are a lot of parameter in user recommendation, which can improve accuracy
*  Allows to customize the buying direction of customers (improved recommendation system)
*  ...
