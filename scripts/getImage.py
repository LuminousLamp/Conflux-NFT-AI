# -*- coding: utf-8 -*
import wenxin_api # 可以通过"pip install wenxin-api"命令安装
from wenxin_api.tasks.text_to_image import TextToImage
import requests
import random
import eel
import json, os
from conflux_web3 import Web3

# eel.init('web')
# eel.start('index.html')





# getImage 函数，在文心大模型上获取图片
# @eel.expose
def getImage(text, style, apikey, secretkey):
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


# invoke函数，将图片上链
def invoke(playerAddress, tokenURI):

    web3 = Web3(Web3.HTTPProvider("https://test.confluxrpc.com"))
    # web3.wallet.add_account(
    #     account := web3.account.from_key(os.environ.get("TESTNET_SECRET"))
    # )
    # web3.cfx.default_account = account.address

    with open('C:/Users/LED/Desktop/nft/scripts/GameItem.json','r')as fp:
        contract_metadata = json.load(fp)
    
    # print(contract_metadata)
    
    nftContract = web3.cfx.contract(
        abi=contract_metadata["abi"], 
        address=contract_metadata["receipt"]["contractCreated"]
        )

    newItemId = nftContract.functions.awardItem(playerAddress, tokenURI)
    print(newItemId)
    # balance = contract.functions.balanceOf(random_account.address).call()
    # balance1 = contract.caller().balanceOf(random_account.address)
    # assert balance1 == balance == 100
    #print(newItemId)

playerAddress = 'cfxtest:aathvsw97m8td0ref0fp5fkzfc0wsrzu0am1k0519x'
tokenURI = 'https://ipfs.io/ipfs/Qmd7uVCXavzXx3sQRzigZsaAQjWa36XnZWhimBwmm7NXC5'
invoke(playerAddress,tokenURI)