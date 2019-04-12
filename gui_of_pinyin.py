'''
基于pyqt5设计的拼音模板客户端软件
立志于提供更佳的用户体验
客户端提供的功能，
         提供拼音模板的制作，提供空白模板用户输入拼音后显示在模板上，最终保存为图片格式
高级功能，提供字数统计，提供不限长度的模板制作（不能使用图片而是使用画线的）
         如果依靠用户使用输入法特殊字符输入比较浪费时间，提供高级功能，给出不同字母的拼音复选框，由用户组合输入
附加功能：提供高级汉字拼音注解功能，上方为注音，下方为汉字，帮助小学生识字
         链接阿里云服务器，实现支付宝转账解锁高级功能
         提供不同的颜色主题
'''
from PyQt5 import QtCore,QtGui,QtWidgets
import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import *
import PIL
from PIL import *
from PyQt5.QtGui import QPixmap,QFontDatabase
from pinyin_png import img as png
import base64
import os
import math
import datetime
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

#定义一个全局的字符串用于预览和向保存函数传递
str = '预览'

class MainUi(QtWidgets.QMainWindow):
    flag = True
    adv_flag = True
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(960, 400)
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格


        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 3)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 4, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.main_layout.setSpacing(0)
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        #左半边的按钮设计
        self.qlabel = QPushButton('拼音模板by Landers')
        self.qlabel.setStyleSheet('''
            QPushButton{
                    border:none;
                    
                    font-size:17px;
                    font-family:"微软雅黑";
                    width:100px;
                    height:40;
                    }''')
        self.bt1 = QPushButton('生成预览')
        self.bt2 = QPushButton('保存模板')
        self.bt3 = QPushButton('自选拼音')
        self.bt4 = QPushButton('注音功能')
        self.bt5 = QPushButton('退出软件')
        self.bt6 = QPushButton('关于软件')
        self.btlist = [self.bt1,self.bt2,self.bt3,self.bt4,self.bt5,self.bt6]


        for n in range(len(self.btlist)):
            self.btlist[n].setStyleSheet('''
                        QPushButton{
                                    border-radius:5px;
                                    border:2px solid black;
                                    color:black;
                                    height:40;
                                    width:150;
                                    background-color:white;
                                    font-size:18px;
                                    font-family:"微软雅黑";
                                    }''')
        self.left_layout.addWidget(self.qlabel, 0, 0, 1, 2)
        self.left_layout.addWidget(self.bt1, 2, 0,1,1)
        self.left_layout.addWidget(self.bt2, 3, 0,1,1)
        self.left_layout.addWidget(self.bt3, 4, 0,1,1)
        self.left_layout.addWidget(self.bt4, 5, 0,1,1)
        self.left_layout.addWidget(self.bt5, 6, 0,1,1)
        self.left_layout.addWidget(self.bt6, 7, 0,1,1)


        #右半边的组件设计
        self.text = QLabel('预览...')
        QFontDatabase.addApplicationFont('pinyin.ttf')
        self.text.setFont(QFont('汉语拼音'))
        pic = QPixmap(r'muban.png')
        self.lbox = QLabel()
        self.lbox.setPixmap(pic)
        self.lb1 = QLabel('下方输入拼音')
        self.lb1.setStyleSheet('''
                    font-size:18px;
                    font-family:"微软雅黑";
                    color:black;
                    ''')
        self.text.setStyleSheet('''
                            font-size:90px;                
                            ''')
        self.textbox = QTextEdit()
        self.textbox.setStyleSheet('''
                    font-size:35px;
                    background-color:white;
                    border:2px solid black;
                    border-radius:15px;
                    padding:0px 8px;
                    font-family:"黑体";
                    
                    ''')
        self.rbt1 = QPushButton('清空内容')
        self.rbt2 = QPushButton('更换背景')
        self.rbt1.setStyleSheet('''
                    font-size:18px;
                    background-color:white;
                    border:2px solid black;
                    border-radius:15px;
                    padding:0px 8px;
                    font-family:"微软雅黑";
                    width:100;
                    height:50;
                    ''')
        self.rbt2.setStyleSheet('''
                    font-size:18px;
                    background-color:white;
                    border:2px solid black;
                    border-radius:15px;
                    padding:0px 8px;
                    font-family:"微软雅黑";
                    width:100;
                    height:50;
                    ''')
        self.rbt3 = QPushButton('高级功能')
        self.rbt3.setStyleSheet('''
                           font-size:18px;
                           background-color:white;
                           border:2px solid black;
                           border-radius:15px;
                           padding:0px 8px;
                           font-family:"微软雅黑";
                           width:100;
                           height:50;
                           ''')
        self.rbt4 = QPushButton('Alipay捐赠')
        self.rbt4.setStyleSheet('''
                                   font-size:18px;
                                   background-color:white;
                                   border:2px solid black;
                                   border-radius:15px;
                                   padding:0px 8px;
                                   font-family:"微软雅黑";
                                   width:100;
                                   height:50;
                                   ''')
        self.status = QPushButton('状态:等待')
        self.status.setStyleSheet('''
                                    font-size:18px;
                                    font:normal;
                                    background-color:rgb(60,179,113);
                                    color:black;
                                    border-radius:5px;
                                    border:2px solid red;
                                    padding:0px 5px;
                                    font-family:"微软雅黑";
                                    width:80;
                                    height:50;
                                           ''')
        self.right_layout.addWidget(self.lbox, 0 ,0, 5, 5)
        self.right_layout.addWidget(self.text, 1, 0, 1, 5)
        self.right_layout.addWidget(self.lb1,5,0,1,5)
        self.right_layout.addWidget(self.textbox,6,0,1,5)
        self.right_layout.addWidget(self.rbt1, 7, 0, 2, 1)
        self.right_layout.addWidget(self.rbt2, 7, 1, 2, 1)
        self.right_layout.addWidget(self.rbt3, 7, 2, 2, 1)
        self.right_layout.addWidget(self.rbt4, 7, 3, 2, 1)
        self.right_layout.addWidget(self.status, 7, 4, 2, 1)




        #界面总体设计
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:rgb(210,180,140);
                border:1px black;
                border-top-right-radius:15px;
                border-bottom-right-radius:15px;
            }
            ''')
        self.left_widget.setStyleSheet('''
                   QWidget#left_widget{
                       color:#232C51;
                       background:rgb(250,250,210);
                       border:1px black;
                       border-top-left-radius:15px;
                       border-bottom-left-radius:15px;
                   }
                   ''')
        self.setStyleSheet('''
                   QInputDialog{
                        border:none;
                        font-size:18px;
                        }''')

        #按钮监听
        self.rbt1.clicked.connect(self.clean) #清空内容
        self.rbt2.clicked.connect(self.changeback)  # 更换主题
        self.rbt3.clicked.connect(self.advanced)  # 激活
        self.rbt4.clicked.connect(self.donate)  # 捐赠
        self.bt1.clicked.connect(self.drawtext) #预览
        self.bt2.clicked.connect(self.save) #保存
        self.bt3.clicked.connect(self.pinyinbox) #自选拼音
        self.bt4.clicked.connect(self.zhuyinbox)  # 自选拼音
        self.bt5.clicked.connect(QCoreApplication.quit)  # 退出
        self.bt6.clicked.connect(self.about) #关于
        self.textbox.textChanged.connect(self.updatetext) #自动更新文本框文字


        #高级功能窗口
        self.zixuan = pinyinzixuan()
        self.zhuyin = zhuyin()
        p = QPixmap(r'a.jpg')
        self.d = QMessageBox(self)
        self.d.setText('支付宝捐赠')
        self.d.setWindowTitle('捐赠')
        self.d.addButton(QPushButton('知道了'),QMessageBox.YesRole)
        self.d.setIconPixmap(p)

    def clean(self):
        global str
        self.textbox.setText(None)
        self.text.setText(None)
        self.zixuan.zhuyinstr = ''
        str = ''
        self.status.setText('状态:已清空')

    def drawtext(self):
        global str
        self.text.setText(str)
        self.status.setText('状态:预览')

    def updatetext(self):
        global str
        str = self.textbox.toPlainText()

    def save(self):
        global str
        num = len(str) / 16
        n = math.ceil(num)
        ls = []
        for i in range(n): #过长自动换行
            ls.append(str[0 + 16 * i:16 + 16 * i])
        tmp = open('pinyin.png', 'wb')
        tmp.write(base64.b64decode(png))
        tmp.close()
        imageFile = "pinyin.png"

        # 初始化参数
        x = 10  # 横坐标（左右）
        y = 17  # 纵坐标（上下）
        word_size = 138  # 文字大小
        try:
            word_css = "pinyin.ttf"
            font = ImageFont.truetype(word_css, word_size)

            # 分割得到数组
            im1 = Image.open(imageFile)  # 打开图片
            draw = ImageDraw.Draw(im1)
            for pstr in ls:
                time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                draw.text((x, y), pstr, (0, 0, 0), font=font)  # 设置位置坐标 文字 颜色 字体
                im1.save(r'C:\\Users\Administrator\Desktop\\{}.png'.format(time))
        except:
            QMessageBox.warning(self,'错误','找不到拼音字体，检查路径')

        del draw  # 删除画笔
        im1.close()  # 关闭图片
        self.status.setText('状态:已保存')
        os.remove('pinyin.png')

    def changeback(self):
        if self.flag:
            self.left_widget.setStyleSheet('''
                    QWidget#left_widget{
                       color:#232C51;
                       background:rgb(123,104,238);
                       border:1px black;
                       border-top-left-radius:15px;
                       border-bottom-left-radius:15px;
                   }
                                   ''')
            self.right_widget.setStyleSheet('''
                    QWidget#right_widget{
                       color:#232C51;
                       background:rgb(70,130,180);
                       border:1px black;
                       border-top-right-radius:15px;
                       border-bottom-right-radius:15px;
                   }
                                    ''')
            self.flag = False
        else:
            self.left_widget.setStyleSheet('''
                    QWidget#left_widget{
                       color:#232C51;
                       background:rgb(250,250,210);
                       border:1px black;
                       border-top-left-radius:15px;
                       border-bottom-left-radius:15px;
                   }
                                               ''')
            self.right_widget.setStyleSheet('''
                    QWidget#right_widget{
                       color:#232C51;
                       background:rgb(210,180,140);
                       border:1px black;
                       border-top-right-radius:15px;
                       border-bottom-right-radius:15px;
                   }
                                                ''')
            self.flag = True

    def about(self):
        QMessageBox.about(self,'关于软件','一个简易的拼音模板客户端\n联系方式：liaorenj@gmail.com')

    def advanced(self):
        code,ok= QInputDialog.getText(self,'激活码','输入激活码')
        codelist = ('16','牛顿','1.38065','2012','APTX4869','lrj','马云')
        if code in codelist:
            self.adv_flag = True

    def donate(self):
        self.d.show()


    def pinyinbox(self):
        if not self.adv_flag:
            QMessageBox.warning(self,'未激活','软件未激活，无法使用高级功能')
        else:
            self.zixuan.show()

    def zhuyinbox(self):
        if not self.adv_flag:
            QMessageBox.warning(self,'未激活','软件未激活，无法使用高级功能')
        else:
            self.zhuyin.show()



class pinyinzixuan(QDialog):
    #定义传递用的注音字符串
    zhuyinstr = ''
    def __init__(self):
        super().__init__()
        self.initui()

    def initui(self):
        self.setWindowTitle('高级声标功能')
        self.setFixedSize(600,500)
        maingrid = QGridLayout()
        self.setLayout(maingrid)
        left = QWidget()
        right = QWidget()
        lgrid = QGridLayout()
        rgrid = QGridLayout()
        left.setLayout(lgrid)
        right.setLayout(rgrid)
        maingrid.addWidget(left,0,0,6,5)
        maingrid.addWidget(right,0,6,6,5)

        list1 = ['ɑ','o','e','i','u','ü'] #韵母
        list2 = ['b','c','d','f','g','h','j','k','l','m','n',\
                'p','q','r','s','t','w','x','y','z','空格'] #声母
        shengmu =[]
        yunmu = []
        self.a = ['a','ā', 'á', 'ǎ', 'à']
        self.o = ['o','ō','ó','ǒ','ò']
        self.e = ['e','ē','é','ě','è']
        self.i = ['i','ī','í','ǐ','ì']
        self.u = ['u','ū','ú','ǔ','ù']
        self.v = ['v','ǖ','ǘ','ǚ','ǜ']
        self.yunflag = 'a'

        for latter ,pos in zip(list1,range(6)):
            bt = QPushButton(latter)
            yunmu.append(bt)
            lgrid.addWidget(bt,1,pos,1,1)

        positions = [(i, j) for i in range(3,7) for j in range(6)]
        for latter ,pos in zip(list2,positions):
            bt = QPushButton(latter)
            shengmu.append(bt)
            lgrid.addWidget(bt,*pos)
        r0 = QPushButton('无音标')
        r1 = QPushButton('1声')
        r2 = QPushButton('2声')
        r3 = QPushButton('3声')
        r4 = QPushButton('4声')
        for r in (r0,r1,r2,r3,r4):
            rgrid.addWidget(r)

        lb1 = QPushButton('韵 母')
        lb2 = QPushButton('声 母')
        lglobal = QPushButton('确定')
        self.showlb = QLabel('预览')
        self.clean = QPushButton('清空')
        self.delete = QPushButton('退格')
        lgrid.addWidget(lb1, 0, 0, 1, 6)
        lgrid.addWidget(lb2, 2, 0, 1, 6)
        lgrid.addWidget(lglobal, 6, 3, 1, 3)
        lgrid.addWidget(self.showlb,7,0,1,8)
        lgrid.addWidget(self.clean,8,0,1,3)
        lgrid.addWidget(self.delete, 8, 3, 1, 3)

        #布局样式管理
        left.setStyleSheet('''  
                    QPushButton{                   
                                border-radius:10px;
                                color:white;
                                background:black;
                                height:50;
                                width:50;
                                font-size:20px;
                                font-family:"黑体"
                                }
                    QPushButton:pressed{
                                background:rgb(32,178,170);  
                                    }
                    QLabel{
                            font-size:25px;
                            background-color:rgb(144,164,96);
                            font-family:"微软雅黑";
                            height:80;
                            }
                            
                                ''')
        right.setStyleSheet('''  
                    QPushButton{                   
                                border-radius:10px;
                                color:black;
                                background:rgb(144,238,144);
                                height:50;
                                width:50;
                                font-size:20px;
                                font-family:"微软雅黑"
                                    }
                    QPushButton:pressed{
                                background:rgb(75,0,130);  
                                    }
                                        ''')
        lb1.setStyleSheet('''
                    background:rgb(95,158,160);
                    color:white;
                    ''')
        lb2.setStyleSheet('''
                            background:rgb(100,149,137);
                            color:white;
                            ''')
        lglobal.setStyleSheet('''
                            QPushButton{background:rgb(100,149,137);
                            color:white;}
                    QPushButton:pressed{background:rgb(75,0,130);}
                            ''')
        #监听
        shengmu[0].clicked.connect(lambda: self.set(shengmu[0]))
        shengmu[1].clicked.connect(lambda: self.set(shengmu[1]))
        shengmu[2].clicked.connect(lambda: self.set(shengmu[2]))
        shengmu[3].clicked.connect(lambda: self.set(shengmu[3]))
        shengmu[4].clicked.connect(lambda: self.set(shengmu[4]))
        shengmu[5].clicked.connect(lambda: self.set(shengmu[5]))
        shengmu[6].clicked.connect(lambda: self.set(shengmu[6]))
        shengmu[7].clicked.connect(lambda: self.set(shengmu[7]))
        shengmu[8].clicked.connect(lambda: self.set(shengmu[8]))
        shengmu[9].clicked.connect(lambda: self.set(shengmu[9]))
        shengmu[10].clicked.connect(lambda: self.set(shengmu[10]))
        shengmu[11].clicked.connect(lambda: self.set(shengmu[11]))
        shengmu[12].clicked.connect(lambda: self.set(shengmu[12]))
        shengmu[13].clicked.connect(lambda: self.set(shengmu[13]))
        shengmu[14].clicked.connect(lambda: self.set(shengmu[14]))
        shengmu[15].clicked.connect(lambda: self.set(shengmu[15]))
        shengmu[16].clicked.connect(lambda: self.set(shengmu[16]))
        shengmu[17].clicked.connect(lambda: self.set(shengmu[17]))
        shengmu[18].clicked.connect(lambda: self.set(shengmu[18]))
        shengmu[19].clicked.connect(lambda: self.set(shengmu[19]))
        shengmu[20].clicked.connect(self.space)
        #lambda函数不能自动更新里面的变量

        lglobal.clicked.connect(self.settobox) #赋值全局变量字符串

        yunmu[0].clicked.connect(lambda: self.setflag(yunmu[0]))
        yunmu[1].clicked.connect(lambda: self.setflag(yunmu[1]))
        yunmu[2].clicked.connect(lambda: self.setflag(yunmu[2]))
        yunmu[3].clicked.connect(lambda: self.setflag(yunmu[3]))
        yunmu[4].clicked.connect(lambda: self.setflag(yunmu[4]))
        yunmu[5].clicked.connect(lambda: self.setflag(yunmu[5]))

        r1.clicked.connect(lambda: self.yinbiao(r1))
        r2.clicked.connect(lambda: self.yinbiao(r2))
        r3.clicked.connect(lambda: self.yinbiao(r3))
        r4.clicked.connect(lambda: self.yinbiao(r4))
        r0.clicked.connect(self.noyinbiao)
        self.clean.clicked.connect(self.cleanstr)
        self.delete.clicked.connect(self.deletestr)

    def set(self,btn):
        self.zhuyinstr = self.zhuyinstr + btn.text()
        #只是为了更新全局字符串
        self.showlb.setText(self.zhuyinstr)

    def space(self):
        #空格
        self.zhuyinstr = self.zhuyinstr + ' '
        self.showlb.setText(self.zhuyinstr)

    def settobox(self):
        global str
        str = self.zhuyinstr

    def setflag(self,btn):
        latter = btn.text()
        if latter == 'a':
            self.yunflag = 'a'
        elif latter =='o':
            self.yunflag = 'o'
        elif latter == 'e':
            self.yunflag = 'e'
        elif latter == 'i':
            self.yunflag = 'i'
        elif latter == 'u':
            self.yunflag = 'u'
        elif latter == 'ü':
            self.yunflag = 'v'

    def cleanstr(self):
        self.zhuyinstr = ''
        self.showlb.setText(self.zhuyinstr)

    def deletestr(self):
        self.zhuyinstr = self.zhuyinstr[:-1]
        self.showlb.setText(self.zhuyinstr)

    def yinbiao(self,btn):
        n = int(btn.text().replace('声', ''))
        lang = self.zhuyinstr
        if self.yunflag == 'a':
            self.zhuyinstr = lang + self.a[n]
        elif self.yunflag == 'o':
            self.zhuyinstr = lang + self.o[n]
        elif self.yunflag == 'e':
            self.zhuyinstr = lang + self.e[n]
        elif self.yunflag == 'i':
            self.zhuyinstr = lang + self.i[n]
        elif self.yunflag == 'u':
            self.zhuyinstr = lang + self.u[n]
        elif self.yunflag == 'v':
            self.zhuyinstr = lang + self.v[n]
        self.showlb.setText(self.zhuyinstr)

    def noyinbiao(self):
        lang = self.zhuyinstr
        if self.yunflag == 'a':
            self.zhuyinstr = lang + self.a[0]
        elif self.yunflag == 'o':
            self.zhuyinstr = lang + self.o[0]
        elif self.yunflag == 'e':
            self.zhuyinstr = lang + self.e[0]
        elif self.yunflag == 'i':
            self.zhuyinstr = lang + self.i[0]
        elif self.yunflag == 'u':
            self.zhuyinstr = lang + self.u[0]
        elif self.yunflag == 'v':
            self.zhuyinstr = lang + self.v[0]
        self.showlb.setText(self.zhuyinstr)

class zhuyin(QDialog):
    def __init__(self):
        super().__init__()
        self.initui()

    def initui(self):
        self.setWindowTitle('汉字注音功能')
        self.setFixedSize(500,500)
        self.imglabel = QLabel()
        self.l = QLabel('我')
        pic = QPixmap(r'tian.jpg')
        self.imglabel.setPixmap(pic)
        QFontDatabase.addApplicationFont('fangzheng.TTC')
        self.l.setFont(QFont('方正楷体拼音字库01'))
        self.imglabel.move(20,10)


        # layout = QVBoxLayout()
        # self.setLayout(layout)


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
