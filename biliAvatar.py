import requests
import os
import logging
from PIL import Image
import json


def getAvatar(uid):
    try:
        url = 'https://api.bilibili.com/x/space/acc/info?mid=%s' % uid
        res = requests.get(url)
        resJson = res.json()
        print("头像url", resJson['data']['face'])
        return resJson['data']['face']
    except Exception as e:
        logging.exception(e)
    
def makImgRound(filename):
    imga = Image.open(filename).convert("RGBA")
    size = imga.size
    minD = min(size)
    r = minD // 2
    minD = r * 2
    imgb = Image.new('RGBA', [minD, minD], (255, 255, 255, 0))
    pima = imga.load()
    pimb = imgb.load()

    x0 = size[0] - minD
    y0 = size[0] - minD
    for i in range(minD):
        for j in range(minD):
            lx = i - r
            ly = j - r
            d = (lx ** 2 + ly ** 2) ** 0.5
            if d <= r:
                pimb[i, j] = pima[x0+i,y0+j]
    
    output = filename[:filename.index('.')] + '.png'
    imgb.save(output)

def enque(uid, uname, filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        candidates = data['candidates']
        infoMap = data['infoMap']

        if len(candidates)>=100:
            uid = candidates.pop(0)
            infoMap.pop(uid)

        dataSet = set(candidates)
        dataSet.add(uid)
        infoMap[uid] = uname
    
    candidates = list(dataSet)
    data['candidates'] = candidates
    data['infoMap'] = infoMap
    with open(filename, 'w', encoding='utf-8') as f:
        data = json.dumps(data, ensure_ascii=False)
        f.write(data)




def downloadAvatar(imgUrl, path, uid):
    os.makedirs(path, exist_ok=True)

    imgName = imgUrl[imgUrl.rindex('/'):]
    filename = '%s/%s%s' % (path, uid, imgName[imgName.index('.'):])

    if os.path.exists(filename):
        return
    
    res = requests.get(imgUrl, stream=True)
    img = res.content
    try:
        with open(filename, 'wb') as f:
            f.write(img)
    except Exception as e:
        logging.exception(e)
    
    makImgRound(filename)

if __name__ == '__main__':
    # makImgRound('data/16479958.jpg')
    enque(1234, 'D:/codes/balls/assets/data/queue.json')