import os
from time import sleep
for duty in range(0, 101, 5):
    os.system(f"sudo gpioset gpiochip0 17=1") 
    sleep(duty*0.0005)
    os.system(f"sudo gpioset gpiochip0 17=0")
    




sleep((100-duty)*0.0005)
i
