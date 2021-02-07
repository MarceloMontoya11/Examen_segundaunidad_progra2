# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 22:28:38 2021

@author: ASUS GAMER
"""
import serial
import threading
import psycopg2
import time
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from kivy.clock import Clock



class proyectoWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        hilo1=threading.Thread(target=self.leer_puerto,daemon=True)
        
        
        hilo1.start()
        
        
        

        self.value_1=0


        Clock.schedule_interval(self.leer_puerto,0.1)
       
    def checkbox_click(self,instance,value):
        pass
    def leer_puerto(self,dt):
            cad=arduino.readline().decode('ascii').strip()
            
            
            if cad:
                pos=cad.index(":")
                label=cad[:pos]
                value=cad[pos+1:]
                if label =='temp':
                    self.ids.temp.text=value
                    
                    
                if label =='lum':
                    self.ids.lumi.text=value

                    
            
            value_temp=self.ids.temp.text
            value_lum=self.ids.lumi.text
            print(value_temp)
            print(value_lum)
            
            insertar_datos(self.ids.temp.text,self.ids.lumi.text)
           
            
    
    def a_cale(self):
        self.value_1=0
        cad='cale:' + str(self.value_1) 
        print(cad)
        arduino.write(cad.encode('ascii'))
    
    def b_cale(self):
        self.value_1=1
        cad='cale:' + str(self.value_1) 
        print(cad)
        arduino.write(cad.encode('ascii'))
    
    def a_foco(self):
        self.value_1=0
        cad='foco:' + str(self.value_1) 
        print(cad)
        arduino.write(cad.encode('ascii'))
    
    def b_foco(self):
        self.value_1=1
        cad='foco:' + str(self.value_1) 
        print(cad)
        arduino.write(cad.encode('ascii'))
    
   
        
def insertar_datos(temperatura,luminosidad):
        
        fecha_actual=time.ctime(time.time())
        sql= """INSERT INTO datos (temperatura,luminosidad,fecha) VALUES(%s,%s,%s);"""
        conn =None
        try:
            conn = psycopg2.connect(
                host     = "localhost",
                database = "proyecto",
                user     = "postgres",
                password = "Mj74758053",
                port     = "5432")   
            cur=conn.cursor()
            cur.execute(sql,(float(temperatura),int(luminosidad),fecha_actual))
            time.sleep(1)
            conn.commit()
            cur.close()
            
            if conn is not None:
                conn.close()
        except(Exception,psycopg2.DatabaseError)as e:
            print("Se encontró un error\n")
            print(e)
        finally:
            if conn is not None:
                conn.close()               
    
              
    

class MainApp(App):
    def build(self):

        return proyectoWindow()

if __name__=='__main__':
   
    try:
        arduino=serial.Serial("COM7",9600,timeout=1)
        
        
        

    except Exception as e:
        exit()
    
    MainApp().run()
    arduino.close()