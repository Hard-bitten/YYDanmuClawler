# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pickle
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import jieba
import codecs

# fin = codecs.open('chatmsg_89703802_10-10-13-17-31.txt',mode = 'r', encoding = 'utf-8')
# print fin.read()

# 第一次运行程序时将分好的词存入文件
text = ''
with open('chatmsg_89703802_10-10-13-17-31.txt') as fin:
    for line in fin.readlines():
        line = line.split('\t')[2]
        text += ' '.join(jieba.cut(line))
        text += ' '
fout = open('text.txt','wb')
pickle.dump(text,fout)
fout.close()

# 直接从文件读取数据
fr = open('text.txt','rb')
text = pickle.load(fr)

# backgroud_Image = plt.imread('bb.jpg')
wc = WordCloud( background_color = 'black',    # 设置背景颜色
                width=2000,height=1600,
                # mask = backgroud_Image,        # 设置背景图片
                max_words = 2000,            # 设置最大现实的字数
                stopwords = STOPWORDS,        # 设置停用词
                font_path = './DroidSansFallbackFull.ttf',# 设置字体格式，如不设置显示不了中文
                max_font_size = 200,            # 设置字体最大值
                random_state = 30,            # 设置有多少种随机生成状态，即有多少种配色方案
                )
wc.generate(text)
# wc.save('./dog.jpg')
# image_colors = ImageColorGenerator(backgroud_Image)
# wc.recolor(color_func = image_colors)
plt.imshow(wc)
plt.axis('off')
plt.savefig("b.png",dpi=300)
plt.show()