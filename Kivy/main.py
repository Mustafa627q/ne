from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel , MDIcon
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFillRoundFlatIconButton,MDFillRoundFlatButton ,MDRectangleFlatButton , MDRaisedButton,MDIconButton,MDFloatingActionButton
from kivymd.uix.button import  MDRectangleFlatButton
from kivy.lang import Builder
from kivy.core.window import Window
from sklearn.model_selection import train_test_split,KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import datetime
import re
import numpy as np
import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt


def dates_before_n_days(n):
    today = datetime.datetime.now()  # الحصول على التاريخ الحالي
    past_date = today - datetime.timedelta(days=n)  # حساب التاريخ قبل n أيام
    
    day = past_date.day  # استخراج اليوم
    month = past_date.month  # استخراج الشهر
    year = past_date.year  # استخراج السنة
    
    return day, month, year




Window.size = (300,600)

KV = '''
ScreenManager:
    MainScreen:
    TimerScreen:
    AiScreen:
<MainScreen>
    name:'main'
    FloatLayout:
        Image:
            source: 'photo_2025-02-14_18-39-34.jpg'
            allow_stretch: True
            keep_ratio:False
        
        MDFillRoundFlatButton:
            id:go to time
            font_name:'28 Days Later'
            text:'Start'
            font_size: 40
            pos_hint:{'center_x':0.5,'center_y':0.3}
            elevation: 100
            on_press: root.manager.current="timer"
        MDFillRoundFlatButton:
            id:analise
            font_name:'28 Days Later'
            text:'AI'
            font_size: 35
            pos_hint:{'center_x':0.5,'center_y':0.2}
            on_press: app.ai()
            
<AiScreen>
    name:'ais'
    FloatLayout:
        Image:
            source:app.sor
            allow_stretch: False
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        MDFillRoundFlatButton:
            text: 'العودة'
            font_name: '28 Days Later'
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
            on_press: root.manager.current = 'main'

<TimerScreen>
    name:"timer"
    FloatLayout:
        Image:
            source: 'photo_2025-02-14_16-21-30.jpg'
            allow_stretch: True
            keep_ratio:False
        MDFillRoundFlatButton:
            id:ma
            text: app.highScore1 
            font_size: 50
            font_name: "digital-7"
            pos_hint: {"center_x": 0.37, "center_y": 0.78}
            size_hint: None, None
            size: "200dp", "200dp"
            radius: [100]
            md_bg_color: 0,0,0,1
        MDFillRoundFlatButton:
            id:hi
            text: app.highScore1 
            font_size: 49
            font_name: "digital-7"
            pos_hint: {"center_x": 0.37, "center_y": 0.78}
            size_hint: None, None
            size: "200dp", "200dp"
            radius: [100]
        MDFillRoundFlatButton:
            id: no
            text: app.start 
            font_size: 35
            font_name: "digital-7"
            pos_hint: {"center_x": 0.75, "center_y": 0.55}
            size: "200dp", "200dp"
            radius: [100]
            md_bg_color: 0,0,0,1
        MDFillRoundFlatButton:
            id:la
            text: app.start 
            font_size: 34
            font_name: "digital-7"
            pos_hint: {"center_x": 0.75, "center_y": 0.55}
            size_hint: None, None
            size: "200dp", "200dp"
            radius: [100]
            md_bg_color: 0/255.0,90/255.0,200/255.0,1
        MDLabel:
            text: 'High Score'
            font_name:"28 Days Later"
            font_size:30
            pos_hint:{'center_x':0.65,'center_y':0.95}
            #theme_text_color:'Custom'
            text_color: 0/255,0.4,1,1
        MDLabel:
            font_name:'ELEGANT TYPEWRITER Bold'
            text:'Timer'
            font_size:20
            pos_hint:{'center_x':1.17,'center_y':0.67}
            #theme_text_color:'Custom'
            text_color: 255/255.0,80/255.0,0/255.0,1
            
            
        MDFillRoundFlatButton:
            id: time
            text: 'Start'
            font_name:"28 Days Later"
            font_size:42
            pos_hint:{'center_x':0.5,'center_y':0.15}
            on_press: app.start_press(self)
            md_bg_color: 0/255,255/255,0/255,1
            
        MDFillRoundFlatButton:
            id: rest 
            text: '5 min Rest'
            font_name:"28 Days Later"
            font_size:35
            pos_hint:{'center_x':0.5,'center_y':5}
            on_press: app.r5minPress()
            md_bg_color: 0/255.0,90/255.0,200/255.0,1
        MDFillRoundFlatButton:
            id: back 
            text: 'Go Back'
            font_name:"28 Days Later"
            font_size:30
            pos_hint:{'center_x':0.5,'center_y':0.05}
            on_press: app.goback()
            md_bg_color: 0/255.0,90/255.0,200/255.0,1
        '''
        
        
        
class AiScreen(Screen):
    pass

class MainScreen(Screen):
    pass
class TimerScreen(Screen):
    pass


screens = ScreenManager()
screens.add_widget(MainScreen(name='main'))  
screens.add_widget(TimerScreen(name='timer'))
screens.add_widget(AiScreen(name='ais'))

       
        
class FoucsApp(MDApp):
    
    sor = StringProperty(None)
    start = StringProperty("\n" + f'00:00:00' +"\n")
    highScore1 = StringProperty(f'\n00:00:00\n')
    
    
    

    
    def build(self):
        self.total_seconds = 0  
        self.hrs=0
        self.mins=0
        self.secs=0
        self.num = 0
        self.timer_event = None
        
        with open('C:/Users/User/Desktop/my python/GUI/Kivy/HighScore.txt', 'r') as high:
            self.highScore = high.read()
            self.highScore= '\n'+self.highScore+'\n'
            self.highScore1= '\n'+(':'.join(re.findall(r'\d{2}',self.highScore)))+'\n'
            
        self.theme_cls.theme_style = 'Light'
        
        
        return Builder.load_string(KV)
    
    
    def ai(self):
        self.all_y = []
        self.all_x=[]
        self.xxx = 0
        
        with open('date.json') as file2:
              data = json.load(file2)
              df = pd.DataFrame(data)
              for x in data :
                  self.index = data.index(x)
                  self.y = 0
                  day_timer = 0
                  if self.index + 1 < len(data):
                    if x['day'] == data[self.index+1]['day'] and x['month']== data[self.index+1]['month']:
                        self.y += x['timer']
                        
                    elif x['day'] == data[self.index-1]['day'] and  x['day'] != data[self.index+1]['day'] and x['month']== data[self.index-1]['month'] :
                        self.y += x['timer']
                    else:
                        self.y += x['timer']
                        self.xxx +=1       
                  else:
                    if x['day'] == data[self.index-1]['day']:
                        self.y += x['timer']
                  self.all_y.append(self.y)
                  self.all_x.append(self.xxx)
        x_train, x_test,y_train,y_test = train_test_split(self.all_x,self.all_y,test_size=0.2)
        x_train = np.array(x_train).reshape(-1, 1)
        x_test = np.array(x_test).reshape(-1, 1)

        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(x_train)
        x_test_scaled = scaler.transform(x_test)

        svr = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
        svr.fit(x_train_scaled, y_train)        

    
        x5 = np.array([self.all_x[-1] + i for i in range(1, 6)]).reshape(-1, 1)
        x5_scaled = scaler.transform(x5)

# توقع القيم
        y_pred = svr.predict(x5_scaled)
        
        plt.plot(self.all_x, self.all_y, label='Focus Time', color='green', ls='-')
        plt.plot(x5, y_pred, label='AI Predict', color='red', ls='--')

        plt.title('Foucs Time')
        plt.xlabel('Days')
        plt.ylabel('Foucs hours')      
        plt.legend()      

        with open('photo.txt','r+')as file:
            file.seek(0)
            s=file.read()
            s_int = int(s)  # تحويل السلسلة إلى عدد صحيح
            s_int += 1     # إضافة 1
            file.seek(0)
            file.write(str(s_int))
        plt.savefig('photo'+str(s),dpi=300,bbox_inches='tight')
        plt.close()
        self.sor = 'photo'+str(s)+".png"
        
        self.root.current = 'ais'
        
        
    
    def goback(self):
        if self.root.current_screen.ids.time.text == 'Stop':
            self.stop_timer()
        if self.root.current_screen.ids.time.text == 'Continue' :
            self.start_press(self.root.current_screen.ids.time)
            self.start_press(self.root.current_screen.ids.time)
        self.root.current = 'main'
    
    def start_press(self,button):
       

                
                      
        if  self.root.current_screen.ids.time.text == 'Stop':
            self.stop_timer()
        elif self.root.current_screen.ids.time.text == 'Start' :
                if self.timer_event:
                    self.stop_timer()
                self.root.current_screen.ids.time.md_bg_color= (255/255.0,0/255.0,0/255.0,1)
                
                
                
                self.root.current_screen.ids.time.pos_hint= {'center_x':0.5,'center_y' : 0.25}
                self.root.current_screen.ids.rest.pos_hint={'center_x':0.5,'center_y':0.15}
                
                self.start_timer(self.update_timer)  
                self.root.current_screen.ids.time.text = 'Stop'
        elif self.root.current_screen.ids.time.text == 'Continue':
                self.total_seconds = 0
                self.stop_timer()
                self.start_timer(self.update_timer)
                self.root.current_screen.ids.time.text = 'Stop'
                self.root.current_screen.ids.time.md_bg_color = 255/255.0,0/255.0,0/255.0,1
                

                
                
    def start_timer(self,fun):
        self.timer_event = Clock.schedule_interval(fun, 1)
        
    def stop_timer(self):
        self.past = []
        if not self.total_seconds > 1:
            if self.timer_event:
                self.timer_event.cancel()
            if self.root.current_screen.ids.time.text == 'Stop':
                
                    high_h, high_m, high_s = map(int, re.findall(r'\d{2}', self.highScore1))
                    try:
                        months_with_31_days = [1,3,5,7,8,10,12]
                        with open ('date.json','r+')as date:
                            lines = json.load(date)
                            self.num = len(lines)  # ✅ عدد المدخلات في القائمة
                                          
                            if int(lines[-1]['year']) == datetime.datetime.now().year:
                                 if int(lines[-1]['month']) == datetime.datetime.now().month:
            
                                   last_day = int(lines[-1]['day']) 
                                   self.last = datetime.datetime.now().day - last_day

                                 elif int(lines[-1]['month']) != datetime.datetime.now().month:
                                   x = datetime.datetime.now().month- int(lines[-1]['month'])
                                   for i in range(x+1):
                                       if i in months_with_31_days:
                                          self.past.append(  datetime.datetime.now().day - 31 + int(lines[-1]['day']))
                                       elif i == 2:
                                            self.past.append (datetime.datetime.now().day - 28 + int(lines[-1]['day']))
                                       else:
                                         self.past.append(  datetime.datetime.now().day - 30 + int(lines[-1]['day']))
                                   self.last = sum(self.past)
                            else:
                                s = datetime.datetime.now().year - int(lines[-1]['year']) 
                                self.last = s*365+ sum(31 if m in months_with_31_days else 30 if m != 2 else 28 for m in range(lines[-1]['month'],13))-lines[-1]['day']+sum(31 if m in months_with_31_days else 30 if m != 2 else 28 for m in range(1,datetime.datetime.now().month))+datetime.datetime.now().day
                                            
                                            
                                
                             
                            date.seek(0) 
                            for n in range(1,self.last):
                                day , month , year = dates_before_n_days(n)
                                lines.append({"year": year,
                                                "month": month,
                                                "day": day ,
                                                "timer": 0,
                                                "last": n} ) 
                            lines.append({"year": datetime.datetime.now().year,
                                                "month":datetime.datetime.now().month,
                                                "day":datetime.datetime.now().day,
                                                "timer": self.hrs+self.mins / 60,
                                                "last": self.last} ) 
                            json.dump(lines, date, indent=4)
                                                       
                    except json.JSONDecodeError:
                          print("حدث خطأ في قراءة الملف. تأكد من أن الملف يحتوي على بيانات صالحة.")
     
                    except FileNotFoundError:
                      with open('date.json', 'w') as date_file:
                        new_entry = {
                        "year": datetime.datetime.now().year,
                        "month": datetime.datetime.now().month,
                        "day": datetime.datetime.now().day,
                        "timer": self.hrs + self.mins / 60,
                        "last": 0}
                    
                        json.dump([new_entry], date_file, indent=4)
                            
                                
                          
                          
                    if (self.hrs, self.mins, self.secs) > (high_h, high_m, high_s):
                        new_high_score = f'{self.hrs:02}:{self.mins:02}:{self.secs:02}'
            
                        with open('C:/Users/User/Desktop/my python/GUI/Kivy/HighScore.txt', 'w') as file:
                            file.write(new_high_score)  
                            self.root.current_screen.ids.hi.text = '\n'+f'{self.hrs:02}:{self.mins:02}:{self.secs:02}'+'\n'
                            self.root.current_screen.ids.ma.text = '\n'+f'{self.hrs:02}:{self.mins:02}:{self.secs:02}'+'\n'
                     
                    self.root.current_screen.ids.time.md_bg_color= (0/255.0,255/255.0,0/255.0,1)

                    self.root.current_screen.ids.time.pos_hint= {'center_x':0.5,'center_y' : 0.15}
                    self.root.current_screen.ids.rest.pos_hint={'center_x':0.5,'center_y':5}
            
                    self.root.current_screen.ids.time.text = 'Start'
                    self.secs = 0
                    self.hrs=0
                    self.mins=0
        else:
            self.timer_event.cancel()
                  
    def update_timer(self,dt):
        print(self.root.ids)
        self.secs += 1
        if self.secs >= 60:
            self.mins += 1
            self.secs = 0
        if self.mins >= 60:
            self.hrs += 1
            self.mins = 0
        high_h, high_m, high_s = map(int, re.findall(r'\d{2}', self.highScore1))
          
        self.root.current_screen.ids.la.text = '\n'+f'{self.hrs:02}:{self.mins:02}:{self.secs:02}'+'\n'
        self.root.current_screen.ids.no.text = '\n'+f'{self.hrs:02}:{self.mins:02}:{self.secs:02}'+'\n'
       
    def r5minPress(self):
     if self.root.current_screen.ids.time.text == 'Stop':  
        self.root.current_screen.ids.time.text = 'Continue'
        self.root.current_screen.ids.time.md_bg_color =  0/255.0,155/255.0,220/255.0,1
        self.stop_timer()
        
     if not self.root.current_screen.ids.time.text =='Start' : 
        if self.total_seconds > 1:
            self.stop_timer()
        self.total_seconds =self.total_seconds+ 300  
        self.h = self.total_seconds // 3600
        self.m = (self.total_seconds % 3600) // 60
        self.s = self.total_seconds % 60
        self.start_timer(self.r5min)

    def r5min(self, dt):
        if self.total_seconds <= 1:  
          self.stop_timer()  # إيقاف المؤقت عند انتهاء العد
          self.start_timer(self.update_timer)  
          if self.root.current_screen.ids.time.text == 'Continue':
              self.root.current_screen.ids.time.text == 'Stop'
  
        self.total_seconds -= 1
        self.h = self.total_seconds // 3600
        self.m = (self.total_seconds % 3600) // 60
        self.s = self.total_seconds % 60

  
        self.root.current_screen.ids.la.text = f'\n{self.h:02}:{self.m:02}:{self.s:02}\n'
        self.root.current_screen.ids.no.text = f'\n{self.h:02}:{self.m:02}:{self.s:02}\n'
print ("hey")
FoucsApp().run()
