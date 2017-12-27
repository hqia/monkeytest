#coding=utf-8
# 引入本程序所用到的模块
import sys,os,datetime
from com.android.monkeyrunner import MonkeyRunner as mr
from com.android.monkeyrunner import MonkeyDevice as md
from com.android.monkeyrunner import MonkeyImage as mi

#配置测试信息 
total_number = 9000    #用例执行最大次数
#定义矩形元组，作为异常特征识别区域
rect = ((222,656,50,55),(900,350,30,20))  #A6
case1 = 'A6-lianjie-duankai'
error_image1 = 'A6Error1.png'


image_path = './monkeytest/framework/Image/screenshot/'
error_image_path = './monkeytest/framework/Image/error/'
case_path = './monkeytest/framework/test_case/'
testLog = './monkeytest/framework/testLog.txt'


#定义Error类，包含错误名字、识别区域、参考图片地址四个属性
class Error(object):
    def __init__(self,name,coordinate,address):
        self.name = name
        self.coordinate = coordinate
        self.address = address
       
error1 = Error('Unable to connect',(222,656,50,55),mr.loadImageFromFile(error_image_path+error_image1)) #A6

#脚本字典
CMD_MAP = {
    'TOUCH': lambda dev, arg: dev.touch(**arg),
    'DRAG': lambda dev, arg: dev.drag(**arg),
    'PRESS': lambda dev, arg: dev.press(**arg),
    'TYPE': lambda dev, arg: dev.type(**arg),
    'WAIT': lambda dev, arg: mr.sleep(**arg),
    'START': lambda dev, arg: dev.startActivity(**arg)
    } 
  
# 执行脚本转换成py语句.
def process_file(fp, device):
    for line in fp:
        (cmd, rest) = line.split('|')
        if cmd == '#':
            print (rest)
            writetestLog(rest)
            continue
        if cmd not in CMD_MAP:
            print ('unknown command: ' + cmd)
            writetestLog('unknown command: ' + cmd)
            continue
        try:
            # Parse the pydict
            rest = eval(rest)
        except:
            writetestLog('unable to parse options')
            print ('unable to parse options')
            continue
        CMD_MAP[cmd](device, rest)

            

        
def writetestLog(tLog):       
    f = open(testLog, 'a')
    f.write(datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')+"    "+tLog+'\n')
    f.close()
    
def checkError(ERR):
#截当前屏幕图片
    nowScreen = device.takeSnapshot()
#截取当前屏幕异常特征识别区域
    ifError = nowScreen.getSubImage(ERR.coordinate)
#用当前图片异常识别区域跟预存的异常特征对比并返回结果
    if(ifError.sameAs(ERR.address, 0.9)):
        print (ERR.name)
        writetestLog(ERR.name)
        return True
    else:
        return False
        
#导出手机log并清除log缓存
def makelog():
    os.system('adb logcat -d > ./monkeytest/framework/log/log.txt')
    os.system('adb logcat -c')
    os.rename('./monkeytest/framework/log/log.txt','./monkeytest/framework/log/'+str(datetime.datetime.now().strftime('%y%m%d-%H%M%S'))+'.txt')

def takescreenshot():
    device.takeSnapshot().writeToFile(image_path+'_'+str(datetime.datetime.now().strftime('%y%m%d-%H%M%S'))+'.png')
        
#播放脚本
def playback(file):
    file = case_path + file
    fp = open(file, 'r')
    process_file(fp, device)
    fp.close()

if(os.path.exists(testLog)): os.remove(testLog)
    
device = mr.waitForConnection()
try:
        device.wake()
except java.lang.NullPointerException, e:
        print >> sys.stderr, "%s: ERROR: Couldn't connect to %s: %s" % (progname, serialno, e)
        sys.exit(3)  


#用于获取识别图片，开始执行测试前需注释掉该段代码
# def getrect():
    # nowScreen = device.takeSnapshot()
    # ifError = nowScreen.getSubImage(rect[0])   
    # ifError.writeToFile(error_image_path+error_image)
# getrect()  
   
#开始测试
for count in range(total_number):
    print(count)
    writetestLog(str(count))
    playback(case1)   
    # if(not checkError(error1)):
        # makelog()   #保存手机打印
        # takescreenshot()   #截图

    
   
   
