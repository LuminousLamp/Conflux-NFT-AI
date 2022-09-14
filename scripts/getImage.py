import wenxin_api
from wenxin_api.tasks.text_to_image import TextToImage
import wenxin_api.error
import requests
import random
import json, os

# getImage 函数，在文心大模型上获取图片
def GetImage(text, style, apikey, secretkey):
    wenxin_api.ak = apikey
    wenxin_api.sk = secretkey


    input_dict = {
        "text": text,
        "style": style
    }
    try:
        imageURLresult = TextToImage.create(**input_dict)
    except(wenxin_api.error.APIError):
        return 'APIError'
    except(wenxin_api.error.APIConnectionError):
        return 'APIConnectionError'
    except:
        return 'error'

    number_of_images = len(imageURLresult['imgUrls'])
    random_index = random.randint(0,number_of_images-1)
    selected_image = imageURLresult['imgUrls'][random_index]
    print(selected_image)

    # img_url为图片链接,
    # file_name为文件储存路径及文件名
    file_name = '../nft/AIpic.jpg'

    res=requests.get(selected_image)
    with open(file_name ,'wb') as f:
        f.write(res.content)
    
    
    return selected_image

# GetImage('','油画','AWla1UImVSbRhtNF7hE0VYv0fekwm9X2','7GB8HPKoV0GvzjyTPTReFffBSu9k93yd')