#coding=utf-8
# 引入本程序所用到的模块
import sys,os,datetime,logging
from com.android.monkeyrunner import MonkeyRunner as mr
from com.android.monkeyrunner import MonkeyDevice as md
from com.android.monkeyrunner import MonkeyImage as mi

testmode = True            #执行测试时为Ture，获取识别图像为False
#配置测试信息 
total_number = 9000    #用例执行最大次数
#定义矩形元组，作为异常特征识别区域
rect = ((222,656,50,55),(900,350,30,20))  #A6
case1 = 'A6-lianjie-duankai'
case2 = 'qiefenbianlv'
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
            logger.info(rest)
            continue
        if cmd not in CMD_MAP:
            logger.info('unknown command: ' + cmd)
            continue
        try:
            # Parse the pydict
            rest = eval(rest)
        except:
            logger.warning('unable to parse options')
            continue
        CMD_MAP[cmd](device, rest)

            

    
def checkError(ERR):
#截当前屏幕图片
    nowScreen = device.takeSnapshot()
#截取当前屏幕异常特征识别区域
    ifError = nowScreen.getSubImage(ERR.coordinate)
#用当前图片异常识别区域跟预存的异常特征对比并返回结果
    if(ifError.sameAs(ERR.address, 0.9)):
        logger.info(ERR.name)
        return True
    else:
        return False
        
#导出手机log并清除log缓存
def getPhoneLog():
    logger.info("get phone log")
    os.system('adb logcat -d > ./monkeytest/framework/phone_log/log.txt')
    os.system('adb logcat -c')
    os.rename('./monkeytest/framework/phone_log/log.txt','./monkeytest/framework/phone_log/'+str(datetime.datetime.now().strftime('%y%m%d-%H%M%S'))+'.txt')

def takescreenshot():
    logger.info("take screenshot")
    device.takeSnapshot().writeToFile(image_path+'_'+str(datetime.datetime.now().strftime('%y%m%d-%H%M%S'))+'.png')
        
#播放脚本
def playback(file):
    file = case_path + file
    fp = open(file, 'r')
    process_file(fp, device)
    fp.close()

    
#配置log    
logger = logging.getLogger('scriptLog')
logger.setLevel(logging.WARNING)  
# 创建一个handler，用于写入日志文件    
fh = logging.FileHandler(testLog)  
# 再创建一个handler，用于输出到控制台    
ch = logging.StreamHandler()
# 定义handler的输出格式formatter    
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
fh.setFormatter(formatter)  
ch.setFormatter(formatter)
logger.addHandler(fh)  
logger.addHandler(ch)     

    
device = mr.waitForConnection()

def getrect(error_image):
    nowScreen = device.takeSnapshot()
    ifError = nowScreen.getSubImage(rect[0])   
    ifError.writeToFile(error_image_path+error_image)
    logger.info("get "+ error_image)

if(testmode):
#开始测试
    logger.info("begin------------------------------")
    for count in range(total_number):
        logger.info(count)
        playback(case2)   
        if(not checkError(error1)):
            getPhoneLog()   #保存手机打印
            takescreenshot()   #截图         
else:
#获取识别图像
    getrect(error_image1)
    

    

    
   
   
