import json
import pprint

from django.db.transaction import atomic

from goodspost.models import *

with open('jiukuaijiu.json', 'r+') as f:
    li = json.loads(f.read())
# print(li)
#
# with open('data.json', 'w') as f:
#     print()
#     f.write(json.dumps(li, indent=2, separators=(',', ':'),ensure_ascii=False))
'''
    "goods":[
      {
        "sizes":[
          [
            "150",
            "150"
          ],
          [
            "160",
            "160"
          ],
          [
            "165",
            "165"
          ],
          [
            "170",
            "170"
          ]
        ],
        "goods_oldprice":"499.00",
        "goods_desc":"梦娜世家2017女式新款修身中长款毛领时尚显瘦欧美气质羽绒服A88",
        "colors":[
          [
            "红色",
            "/media/color/hong_Dm4fQ6U.jpg"
          ],
          [
            "绿色",
            "/media/color/lv_cTMJg2K.jpg"
          ],
          [
            "黄色",
            "/media/color/huang_bvCMlhn.jpg"
          ],
          [
            "黑色",
            "/media/color/hei_rFOWelp.jpg"
          ]
        ],
        "goodsname":"90绒大毛领保暖羽绒服",
        "goods_price":"99.00",
        "specs":[
          [
            "参数规格",
            [
              "/static/img/%E8%AF%A6%E6%83%85%E9%A1%B5_03.png"
            ]
          ],
          [
            "整体款式",
            [
              "/static/img/%E8%AF%A6%E6%83%85%E9%A1%B5_06.png"
            ]
          ],
          [
            "模特实拍",
            [
              "/media/1_mpwtoGA.jpg",
              "/media/2_UuQkY4b.jpg",
              "/media/3_ViMgWv6.jpg",
              "/media/4_BDmgdFv.jpg",
              "/media/5_ozWIsej.jpg",
              "/media/6_Pny8yTQ.jpg",
              "/media/7_K4tB09L.jpg",
              "/media/8_60MJMwS.jpg",
              "/media/9_8YomGSk.jpg",
              "/media/10_vonnLjk.jpg"
            ]
          ]
        ]
      },
      
      goods_name, goods_oldprice ,goods_desc, color, sizes, specs, goods_price
'''

@atomic
def installdata(li):
    for cat in li:
        cate = Category.objects.create(cname=cat.get('catefory', ''))
        for gds in cat.get('goods'):
            if gds:
                goods = Goods.objects.create(gname=gds.get('goods_name'), cate=cate, gdesc=gds.get('goods_desc')
                                             , price=gds.get('goods_price'), oldprice=gds.get('goods_oldprice'))
                for sizes in gds.get('sizes'):
                    size = Gsize.objects.create(sname=sizes[0])
                    for colors in gds.get('colors'):
                        color = Gcolor.objects.create(colorname=colors[0], colorurl=colors[1])
                        Inventory.objects.create(color=color, size=size, goods=goods)
                for gdetail in gds.get('specs'):
                    gdetailname = Goodsdname.objects.create(gdname=gdetail[0])
                    for gdurl in gdetail[1]:
                        Goodsdetail.objects.create(gdetailname=gdetailname, gdurl=gdurl, goods=goods)

installdata(li)

