from MyControllers import FuzzyController

import matplotlib.pyplot as plt
from random import random
from tqdm import tqdm

if __name__=="__main__":
	fc = FuzzyController()
	#fc.show(True)
	T=[21,21,21]
	x=[]
	y=[]
	for i in tqdm(range(100)):
		k1=random()+1
		k2=random()+1
		k3=random()+1
		if fc.compute(T)<0.5:
			T=[max(21,T[0]-k1),max(21,T[0]-k2/9),max(21,T[0]-k3/36)]
		else:
			T=[min(100,T[0]+k1),min(100,T[0]+k2/9),min(100,T[0]+k3/36)]
		x=x+[i]
		y=y+[T]
		
	plt.figure()
	plt.plot(x,y)
	plt.show()
	
	#input('Press ENTER to exit')
