import numpy as np
import pandas as pd
import os
import sys
import math


image_model = "static/data/model_maithuy.xlsx"
image_not_availble = "static/images/noimage.jpg"
uploadFolder = "https://maithuy.com/Upload/Image/Model/100/"
dataframe = pd.read_excel(image_model)


def renderImage(productid):
    df = dataframe
    html_str = ""
    tmp = df[df["Id"] == productid]["Image"].values
    tmp2 = df[df["Id"] == productid]["SeoName"].values
    if tmp.shape[0] > 0:
        image_url = uploadFolder + tmp[0]
        html_str += (
            "<div class='col-xs-2'><figure>"
            + "<a href='https://maithuy.com/model/May-phay-duc-tuong-Macroza-M-95-"
            + str(int(productid))
            + "'>"
            + " <img  class='border' src='"
            + image_url
            + "' width='140' height='140'/></a>"
        )
        if tmp2.shape[0] > 0:
            html_str += "<figcaption>" + tmp2[0] + "</figcaption>"
        html_str += "</figure></div>"
    else:
        image_url = image_not_availble
        html_str += (
            "<div class='col-xs-2'><figure>"
            + "<a href='https://maithuy.com/model/May-phay-duc-tuong-Macroza-M-95-"
            + str(int(productid))
            + "'>"
            + " <img  class='border' src='"
            + image_url
            + "' width='140' height='140'/></a>"
        )
        if tmp2.shape[0] > 0:
            html_str += "<figcaption>" + tmp2[0] + "</figcaption>"
        else:
            html_str += "<figcaption> Sản phẩm mã số <b>" + str(int(productid))+"</b> đã cũ, không có thông tin </figcaption>"
        html_str += "</figure></div>"

    return html_str

def renderImage2(productid):
    df = dataframe
    html_str = ""
    tmp = df[df["Id"] == productid]["Image"].values
    tmp2 = df[df["Id"] == productid]["SeoName"].values
    if tmp.shape[0] > 0:
        image_url = uploadFolder + tmp[0]
        html_str += (
            "<div class='col-xs-2'><figure>"
            +"<a href='https://maithuy.com/model/May-phay-duc-tuong-Macroza-M-95-"
            + str(int(productid))
            + "'>"
            + " <img  class='border' src='"
            + image_not_availble
            + "' width='140' height='140'/></a>"
        )
        if tmp2.shape[0] > 0:
            html_str += (
                "<figcaption>"
                + tmp2[0]
                + "</figcaption>"
            )
        html_str+="</figure></div>"
    return html_str