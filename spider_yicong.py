import  requests
import os
import re
from lxml import etree
from bs4 import BeautifulSoup
from PIL import Image
import time 
from io import BytesIO
import threadpool


headers = {
    'Host': 'www.yczihua.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Cookie': 'real_ipd=202.115.12.166; 53gid2=11021424921012; 53revisit=1540114682980; Hm_lvt_bf0436dd7207e10763d8dde61dc884c6=1540114695,1540369586,1540435160; 53gid1=11021424921012; visitor_type=old; 53gid0=11021424921012; 53kf_70851558_from_host=www.yczihua.com; 53kf_70851558_keyword=http%3A%2F%2Fwww.yczihua.com%2Fhuaniao%2F; 53kf_70851558_land_page=https%253A%252F%252Fwww.yczihua.com%252F; kf_70851558_land_page_ok=1; Hm_lpvt_bf0436dd7207e10763d8dde61dc884c6=1540438913; 53uvid=1; onliner_zdfq70851558=0; YC_ID=0540fb0b05a56105d9f4af245ee470dff8e23fa1; ECS[history]=11277%2C3458%2C11848%2C7957; invite_53kf_totalnum_1=3',
    'Connection': 'close',
    'Upgrade-Insecure-Requests':'1'

}

def save_img(url,path):
    res = requests.get(url,headers=headers,allow_redirects=False,verify=False)
    image = Image.open(BytesIO(res.content))
    #print(path)
    image.save(path)



def get_info(i):
    print(i)
    url="http://www.yczihua.com/goods-{0}.html".format(i)
    r = requests.get(url,headers=headers,allow_redirects=False,verify=False)
    code = r.status_code
    if code == 200:
        content = BeautifulSoup(r.content,"lxml")
        #code,author,type,path

        print(url)
        if len(content.select('.parameter dd')):
            pic_type = content.select('.parameter dd')[1].text
        else :
            return 0
        dir  ='../data/'
        if '山水' in pic_type:
            pic_type = 'mountains'
            dir = dir + 'mountains/'
            if not os.path.exists(dir):
                os.makedirs(dir)
        elif '花鸟' in pic_type:
            pic_type = 'flowers'
            dir = dir + 'flowers/'
            if not os.path.exists(dir):
                os.makedirs(dir)
        elif '人物' in pic_type:
            pic_type = 'persons'
            dir = dir + 'persons/'
            if not os.path.exists(dir):
                os.makedirs(dir)
        elif '动物' in pic_type:
            pic_type = 'animals'
            dir = dir + 'animals/'
            if not os.path.exists(dir):
                os.makedirs(dir)
        else:
            pic_type = 'others'
            dir = dir + 'others/'
            if not os.path.exists(dir):
                os.makedirs(dir)
        print(pic_type)
        try:
            pic_url=content.select('#goods_img_0_0')
            pic_1 ='http://'+ re.findall(r'//(.+?)"',str(pic_url[0]))[0]
            pic_name_1 = re.findall(r'goods_img/(.+?)"',str(pic_url[0]))[0]
            path_1 = dir + pic_name_1
            save_img(pic_1,path_1)
        except:
            pass
        try:
            pic_url=content.select('#goods_img_1_1')
            pic_2 ='http://'+ re.findall(r'//(.+?)"',str(pic_url[0]))[0]
            pic_name_2 = re.findall(r'goods_img/(.+?)"',str(pic_url[0]))[0]
            path_2 = dir + pic_name_2
            save_img(pic_2,path_2)
        except:
            pass
    else:
        print('error url !!!')


def main():
    pool = threadpool.ThreadPool(20)
    reqs = threadpool.makeRequests(get_info,range(1,20000))
    [pool.putRequest(req) for req in reqs]
    pool.wait()


if __name__ == "__main__":
    main()