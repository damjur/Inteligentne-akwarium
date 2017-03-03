from MyControllers import FuzzyController

def read_temp(name):
	temp = 23000
	try:
		with open('/sys/bus/w1/devices/' + name + '/w1_slave') as sensor:
			for i,line in enumerate(sensor):
				if i==0:
					if line.split(' ')[-1] == "NO":
						break
				else:
					temp = int(line.split(' ')[-1][2:])
	finally:
		return temp/1000

if __name__=='__main__':
	
	while True:
		print(0,read_temp('28-0416a4ac2eff'))
		print(1,read_temp('28-0516a41864ff'))
		print(2,read_temp('28-0916a4ac2eff'))
				