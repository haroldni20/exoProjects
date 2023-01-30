# Modulos necesarios

import network, time, urequests
from machine import Pin, PWM, ADC
from utelegram import Bot
from utime import sleep, sleep_ms

# TOKEN Obtenido desde BotFather para usar desde Telegram

TOKEN = '5640425340:AAEWkAI6hqwkvSpK5-eSzMEGcYqitkHB_Sk'

# Declaracion de objetos (Servomotor y Galga extensiometrica)

bot = Bot(TOKEN)
servoUp = PWM(Pin(21), freq=50)
#sensorP = ADC(Pin(34))

# Funcion Servo
def map_s(x):
    return int((x - 0) * (2400000- 500000) / (180 - 0) + 500000) # v1.19 --duty_ns() --0 y 1_000_000_000

#Funcion para conexión WIFI

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True
    
#Bot Telegram
    
if conectaWifi ("Vargas Castillo", "Jack2020"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    print("ok")
    
    
    @bot.add_message_handler("Hola")
    def help(update):
        update.reply("¡Hola! Bienvenido a ExoProject, a continuación estará nuestro menú para hacer funcionar tu exoesqueleto: Escribe Activar Exoesqueleto para encenderlo o Apagar Exoesqueleto para finalizar la tarea")

    @bot.add_message_handler("Activar Exoesqueleto")
    def help(update):
        lectura = int(32767.5*180/65535) #El numero 32767.5 esta dado para el movimiento a 90°
        angulo = (lectura+45)*100000/9
        servoUp.duty_ns(int(angulo))
        print("Movimiento a: {}° ".format(lectura))
        sleep_ms(10)
        update.reply("Encendido a 90° \U0001F600 Recuerda activarlo para inmovilizar y mejorar la reconstrucción de tu tendón")

    @bot.add_message_handler("Apagar Exoesqueleto")
    def help(update):
        lectura = int(0.0*180/65535) #El numero 0.0 esta dado para el movimiento a 0°
        angulo = (lectura+45)*100000/9
        servoUp.duty_ns(int(angulo))
        print("Movimiento a: {}° ".format(lectura))
        sleep_ms(10)
        update.reply("El Exoesqueleto se ha apagado \U0001F636 Descansa un poco")

    bot.start_loop()

else:
    print ("Imposible conectar")
    miRed.active (False)
