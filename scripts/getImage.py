import wenxin_api
from wenxin_api.tasks.text_to_image import TextToImage
import requests
import random
import eel
import json, os
from conflux_web3 import Web3

# getImage 函数，在文心大模型上获取图片
# @eel.expose
def GetImage(text, style, apikey, secretkey):
    wenxin_api.ak = apikey
    wenxin_api.sk = secretkey


    input_dict = {
        "text": text,
        "style": style
    }
    imageURLresult = TextToImage.create(**input_dict)
    # print(imageURLresult)
    # print(imageURLresult['imgUrls'])
    number_of_images = len(imageURLresult['imgUrls'])
    random_index = random.randint(0,number_of_images-1)
    selected_image = imageURLresult['imgUrls'][random_index]
    print(selected_image)

    # img_url为图片链接,
    # file_name为文件储存路径及文件名
    file_name = 'AIpic.jpg'

    res=requests.get(selected_image)
    with open(file_name ,'wb') as f:
        f.write(res.content)