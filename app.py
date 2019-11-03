from flask import Flask, render_template, request
import os
from static.utils import item_recommendation
import numpy as np

app = Flask(__name__)

@app.route('/modellist')
def modellist():
    return render_template("modellist.html", **locals())

@app.route("/user")
def user_rec():
    return render_template("user_rec.html")

@app.route("/")
def home():
    return render_template("item_rec.html")


@app.route("/item")
def item_rec():
    itemid = request.args.get('id')
    itemid = 6 if itemid == '' else itemid
    item_list = ''
    if(itemid != None):
        itemid = int(itemid)
        item_list = item_recommendation.get_recommendation_by_id(itemid)

        nplist = np.zeros((2,10))
        print(type(item_list.keys()[0]))
        nplist[0] = item_list.keys()
        nplist[1] = item_list.values
        print(nplist.shape)
        item_list = nplist
        item_del = np.delete(item_list, 0, 1)

        html_str = '<ul>'
        for (x,y) in np.ndenumerate(item_del[0]):
            html_str += '<li> <a href="https://maithuy.com/model/May-phay-duc-tuong-Macroza-M-95-' + str(int(y)) +'">'+ str(int(y)) + ' </a></li>'
        html_str += '</ul>'

    return render_template("item_rec.html", **locals())


# @app.route("/test/<filename>")
# def test(filename):
#     # filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     # imageResult = image_util.detect_object(filename)
#     # return redirect(url_for('render_image', filename=imageResult))
#     # user_image = image_util.detect_object(filename)
#     return render_template('imageShow.html', **locals())



# @app.route('/upload/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

# @app.route('/<filename>')
# def render_image(filename):
#     user_image = os.path.join(TEST_RESULT_PATH, filename)
#     return render_template('imageShow.html', **locals())

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and upload_util.allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('test', filename=filename))
#         return redirect(request.url)
#     if request.method == 'GET':
#         return render_template("upload.html")



if __name__ == "__main__":
    app.run(debug=True)
