from flask import Flask, render_template, request, redirect
import os
from static.utils import recommendation as recommendationUtil
import numpy as np

app = Flask(__name__)

@app.route('/modellist')
def modellist():
    return render_template("modellist.html", **locals())

@app.route("/user", methods=['GET', 'POST'])
def user_rec():
    requestList = request.args.get('id')
    requestList = "" if requestList == None else requestList
    if(requestList != ""):
        item2array = requestList.split()
        try: 
            recommendationList = recommendationUtil.get_recommendation_by_list_of_id(item2array)
            nplist = np.transpose(recommendationList.values)
            # print(recommendationList.values.shape)
            # nplist[0] = recommendationList.keys()
            # nplist[1] = recommendationList.values
            # recommendationList = nplist
            item_del = np.delete(nplist, 0, 1)
            # html_str = recommendationList
            html_str = '<ul>'
            for (x,y) in np.ndenumerate(item_del[0]):
                html_str += '<li> <a href="https://maithuy.com/model/May-phay-duc-tuong-Macroza-M-95-' + str(int(y)) +'">'+ str(int(y)) + ' </a></li>'
            html_str += '</ul>'
        except:
            html_str = "Nhập sai thông tin mã số sản phẩm - mã sản phẩm chỉ gồm list các số cách nhau bằng 1 dấu space !!!"
    else:
        html_str = "Hãy nhập thôn tin vào textbox ở trên"
    # print(itemlist)
    

    return render_template("user_rec.html", **locals())

@app.route("/")
def home():
    return redirect("/item", code=302)


@app.route("/item", methods=['GET', 'POST'])
def item_rec():
    requestId= request.args.get('id')
    requestId = "" if requestId == None else requestId
    # requestId = 6 if requestId == '' else requestId
    recommendationList = ''
    if(requestId != ""):
        try:
            requestId = int(requestId)
            recommendationList = recommendationUtil.get_recommendation_by_id(requestId) 
            nplist = np.zeros((2,10))
            nplist[0] = recommendationList.keys()
            nplist[1] = recommendationList.values
            recommendationList = nplist
            item_del = np.delete(recommendationList, 0, 1)

            html_str = '<ul>'
            for (x,y) in np.ndenumerate(item_del[0]):
                html_str += '<li> <a href="https://maithuy.com/model/May-phay-duc-tuong-Macroza-M-95-' + str(int(y)) +'">'+ str(int(y)) + ' </a></li>'
            html_str += '</ul>'
        except:
            html_str = "Mã sản phẩm không tồn tại!!!"
    else:
        html_str = "Hãy nhập thông tin vào textbox ở trên"
        
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
    app.run(debug=True, host = '0.0.0.0')
