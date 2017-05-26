from MyControllers import FuzzyController
import RPi.GPIO as GPIO  

def read_temp(name, temp):
	try:
		with open('/sys/bus/w1/devices/' + name + '/w1_slave') as sensor:
			for i,line in enumerate(sensor):
				if i==0:
					if line.split(' ')[-1] == "NO":
						break
				else:
					x = int(line.split(' ')[-1][2:])
					if 100 < x < 85000:
						temp = x
	finally:
		return temp/1000

if __name__=='__main__': 
	try:
		T = [];
		fc = FuzzyController()
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(11, GPIO.OUT) 
		for i in range(3):
	                T.append(23)
		while True:
			T[0] = (read_temp('28-0416a4ac2eff', T[0]*1000))
			T[1] = (read_temp('28-0516a41864ff', T[1]*1000))
			T[2] = (read_temp('28-0416a4aeaaff', T[2]*1000))
			print(T)
			x = fc.compute(T)
			print(x)
			if x > 0.5:
				GPIO.output(11,GPIO.LOW)
			else:
				GPIO.output(11,GPIO.HIGH)
	finally:
		GPIO.output(11, GPIO.HIGH)
		GPIO.cleanup()
                        
                        
				
