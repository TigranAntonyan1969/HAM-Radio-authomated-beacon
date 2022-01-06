import time
from machine import Pin, PWM

led_onboard = machine.Pin(25, machine.Pin.OUT)
tx_signal = machine.Pin(14, machine.Pin.OUT)
sound = machine.PWM(machine.Pin(15))
sound.freq(1000)
sound.duty_u16(200) 


morse= {
    "A": ".-!",
    "B": "-...!",
    "C": "-.-.!",
    "D": "-..!",
    "E": ".!",
    "F": "..-.!",
    "G": "--.!",
    "H": "....!",
    "I": "..!",
    "J": ".---!",
    "K": "-.-!",
    "L": ".-..!",
    "M": "--!",
    "N": "-.!",
    "O": "---!", 
    "P": ".--.!",
    "Q": "--.-!",
    "R": ".-.!",
    "S": "...!",
    "T": "-!",
    "U": "..-!",
    "V": "...-!",
    "W": ".--!",
    "X": "-..-!",
    "Y": "-.--!",
    "Z": "--..!",
    "1": ".----!",
    "2": "..---!",
    "3": "...--!",
    "4": "....-!",
    "5": ".....!",
    "6": "-....!",
    "7": "--...!",
    "8": "---..!",
    "9": "----.!",
    "0": "-----!",
    " ": " ",
}

#Вводим исходные данные
textin='R2AVZ BEACON TEST 1W QTH KO85RT50' #Сообщение которое будет передаваться маяком (заглавными латинскими)
TimeTX=60 #Желаемая длительность времени передачи в один сеанс в секундах
CycleTime=360 #Длтельность одного цикла: передача и молчание, тоже в секундах
S=0.5 #Коэффициент регулирующий скорости передачи

#Расчёт количества знаков и пробелов в сообщении
B=len(textin)

#Конвертация сообщения в сообщение передаваемое азбукой Морзе
i=0 
Message=""
for i in range(B):
    Message=Message+morse[textin[i]]  
print(Message)

#Количество знаков в сообщении уже преобразованном в азбуку Морзе
A=len(Message)

#Расчёт длительности одного сообщения передаваемого азбукой Морзе в секундах
count = {}
for character in Message:
    count.setdefault(character, 0)
    count.setdefault(' ', 0) # на случай если сообщение не будет содержать пробелов
    count[character] = count[character] + 1
print(count)
Duration=count.get('-')*0.3*S + count.get('!')*0.2*S + count.get(' ')*0.4*S + count.get('.')*0.1*S + 0.7*S
print(Duration)

#Расчет целого количества повторений сообщения за время передачи в одном цикле
Repeat=TimeTX/Duration
print(int(Repeat))

#Расчёт реальной длительности передачи целого количества сообщений
TimeTXReal=int(Repeat)*Duration
print(TimeTXReal)

#Расчёт времени молчания маяка в одном цикле в секундах
SilenceTime=CycleTime - TimeTXReal
print(SilenceTime)

#Тело цикла
k=0
while True:
    if k<Repeat:
        k=k+1
        time.sleep(0.7*S)
        i=0
        for i in range(A):
            if Message[i]=='-':
                led_onboard.value(1)
                tx_signal.value(1)
                sound.duty_u16(100000)
                time.sleep(0.3*S)
                led_onboard.value(0)
                tx_signal.value(0)
                sound.duty_u16(1)
                time.sleep(0.1*S)            
            elif Message[i]=='.':
                led_onboard.value(1)
                tx_signal.value(1)
                sound.duty_u16(100000)
                time.sleep(0.1*S)
                led_onboard.value(0)
                tx_signal.value(0)
                sound.duty_u16(1)
                time.sleep(0.1*S)
            elif Message[i]=='!':
                led_onboard.value(0)
                tx_signal.value(0)
                time.sleep(0.2*S)
            else:
                led_onboard.value(0)
                tx_signal.value(0)
                time.sleep(0.4*S)
    else:
        time.sleep(SilenceTime)
        k=0
        continue
    