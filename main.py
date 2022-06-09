import streamlit as st
import io
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

textcolor = 'white'
textsize = 40

st.title('顔認識アプリ')

subscripton_key = 'f5c1da89cdf5450eaeddabbec06866c8'
assert subscripton_key
face_api_url = 'https://macbook-tanaka220608.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader('Choose an image...',type='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img.save(output,format='JPEG')
        binary_img = output.getvalue()
    headers = {
        'Content-Type':'application/octet-stream',
        'Ocp-Apim-Subscription-Key' : subscripton_key
        }
    params = {
        'retrunFaceId':'true',
        'returnFaceAttributes': 'blur,exposure,noise,age,gender,facialhair,glasses,hair,makeup,accessories,occlusion,headpose,emotion,smile'
    }
    res = requests.post(face_api_url,params=params,headers=headers,data = binary_img)
    results = res.json()
    url = 'https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300&display=swap'
    font = ImageFont.truetype('NotoSansJP-Medium.otf', size=textsize)
    for result in results:
        rect = result['faceRectangle']
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline='red',width=4)
        age = str(result['faceAttributes']['age'])
        gender = result['faceAttributes']['gender']
        text = '年齢: '+age+'歳、性別: '+gender
        txpos = (rect['left'], rect['top']-textsize)
        draw.text(txpos, text,font= font,fill=textcolor)
    st.image(img,caption='Uploaded Image.',use_column_width = True)








