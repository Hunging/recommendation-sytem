from flask import Flask, render_template, request, redirect
import os
from static.utils import recommendation as recommendationUtil
from static.utils import template as templateUtil
import numpy as np
import pandas as pd

app = Flask(__name__)
image_model = "static/data/model_maithuy.xlsx"
uploadFolder = "https://maithuy.com/Upload/Image/Model/100/"


def getDataFrame():
    dataframe = pd.read_excel(image_model)
    return dataframe


@app.route("/modellist")
def modellist():
    return render_template("modellist.html", **locals())


@app.route("/user", methods=["GET", "POST"])
def user_rec():
    requestList = request.args.get("id")
    requestList = "" if requestList == None else requestList
    if requestList != "":
        item2array = requestList.split()
        try:
            recommendationList = recommendationUtil.get_recommendation_by_list_of_id(
                item2array
            )
            nplist = np.transpose(recommendationList.values)
            item_del = np.delete(nplist, 0, 1)

            df = getDataFrame()
            html_str = "<span>"
            html_str = "<div class='container'>"
            html_str += "<h3> Input item: </h3>"
            for i in item2array:
                html_str += templateUtil.renderImage(int(i))

            html_str += "</div>"
            html_str += "<div class='container'>"
            html_str += "<h3> Our recommendation: </h3>"
            html_str += "<div class='row h-50'>"
            count = 0
            for (x, y) in np.ndenumerate(item_del[0]):
                count = count +1
                if count % 6 == 0:
                    html_str += "</div><div class='row h-50'>"
                html_str += templateUtil.renderImage(int(y))
            html_str += "</div>"
            html_str += "</span>"
        except:
            html_str = "Nhập sai thông tin mã số sản phẩm - mã sản phẩm chỉ gồm list các số cách nhau bằng 1 dấu space !!!"
    else:
        html_str = "Hãy nhập thông tin vào textbox ở trên"

    return render_template("user_rec.html", **locals())


@app.route("/")
def home():
    return redirect("/item", code=302)


@app.route("/item", methods=["GET", "POST"])
def item_rec():
    requestId = request.args.get("id")
    requestId = "" if requestId == None else requestId
    recommendationList = ""
    if requestId != "":
        templateUtil.renderImage(requestId)
        try:
            requestId = int(requestId)
            recommendationList = recommendationUtil.get_recommendation_by_id(requestId)
            nplist = np.zeros((2, 10))
            nplist[0] = recommendationList.keys()
            nplist[1] = recommendationList.values
            recommendationList = nplist
            item_del = np.delete(recommendationList, 0, 1)
            df = getDataFrame()
            html_str = "<div class='container'>"
            html_str += "<h3> Input item: </h3>"
            html_str += templateUtil.renderImage(requestId)
            
            html_str += "</div>"
            html_str += "<div class='container'>"
            html_str += "<h3> Our recommendation: </h3>"
            html_str += "<div class='row h-50'>"
            count = 0
            for (x, y) in np.ndenumerate(item_del[0]):
                count = count +1
                if count % 6 == 0:
                    html_str += "</div><div class='row h-50'>"
                html_str += templateUtil.renderImage(y)
            html_str += "</div>"
            html_str += "</div>"
        except:
            print("loi roi")
            html_str = (
                "Mã sản phẩm không tồn tại hoặc chưa ai mua sản phẩm này bao giờ!!!"
            )
    else:
        html_str = "Hãy nhập thông tin vào textbox ở trên"

    return render_template("item_rec.html", **locals())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

