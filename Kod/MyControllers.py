#zrobiæ kwargs



import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

class FuzzyController:
	def __init__(self,T=40,T0=21,dT=10,precision=1,number=3):
		# T - temperatura docelowa
		# T0 - temperatura otoczenia
		# dT - maksymalne wachanie temperatury
		# precision - dok³adnoœæ pomiaru
		# number - liczba czujników
		
		#od uchybu temperatury otoczenia do temp. wrzenia
		universe = np.arange(T0-T,100-T+precision,precision)
		u2 = np.arange(0,1.02,0.02)
		self.T = T
		#print("Setting up membership functions")
		
		self.errors = [ctrl.Antecedent(universe, 'error'+str(i)) for i in range(number)]
		self.deltas = [ctrl.Antecedent(universe, 'delta'+str(i)) for i in range(number)]
		self.output = ctrl.Consequent(u2,'on_off')
		
		for i in range(number):
			self.errors[i]['cold'] = fuzz.trapmf(universe,[T0-T,T0-T,-dT,0])
			self.errors[i]['hot'] = fuzz.trapmf(universe,[0,dT,100-T,100-T])
			self.errors[i]['perfect'] = fuzz.trimf(universe,[-dT,0,dT])
			
			# nb - negative 
			# ze - zero
			# pb - positive
			d = min(T-T0,100-T)
			self.deltas[i]['nb'] = fuzz.trapmf(universe,[T0-T,T0-T,-dT,0])
			#self.deltas[i]['ns'] = fuzz.trimf(universe,[-dT,-dT/2,0])
			#self.deltas[i]['ze'] = fuzz.trimf(universe,[-dT,0,dT])
			#self.deltas[i]['ps'] = fuzz.trimf(universe,[0,dT/2,dT])
			self.deltas[i]['pb'] = fuzz.trapmf(universe,[0,dT,100-T,100-T])
		
		self.output['off'] = fuzz.trimf(u2,[0,0,1])
		self.output['on'] = fuzz.trimf(u2,[0,1,1])
		
		#print("Setting up rules and control system")
		
		self.rules = []
		for i in range(number):
			rule1 = ctrl.Rule(self.errors[i]['cold'],self.output['on'])
			rule2 = ctrl.Rule(self.errors[i]['hot'],self.output['off'])
			rule3 = ctrl.Rule(self.errors[i]['perfect'] & (self.deltas[i]['pb']),self.output['off'])
			#rule31 = ctrl.Rule(self.errors[i]['perfect'] & (self.deltas[i]['ps']),self.output['on'])
			rule4 = ctrl.Rule(self.errors[i]['perfect'] & (self.deltas[i]['nb']),self.output['on'])
			#rule41 = ctrl.Rule(self.errors[i]['perfect'] & (self.deltas[i]['ns']),self.output['on'])
			#rule5 = ctrl.Rule(self.errors[i]['perfect'] & (self.deltas[i]['ze']),self.output['on'])
			
			self.rules = self.rules + [
				rule1,
				rule2,
				rule3,
				rule4,
				#rule41,
				#rule31,
				#rule5
			]
		
		self.control_system = ctrl.ControlSystemSimulation(ctrl.ControlSystem(self.rules))
		
		#print("Initializing variables")
		
		self.e = np.array([T0-T for i in range(number)])
		self.de = np.zeros(number)

		
	def show(self,flag=False):
		if flag:
			self.errors[0].view()
			self.deltas[0].view()
			self.output.view()
		
		for rule in self.rules:
			print(rule)
			
		#self.output.view(sim=self.control_system)
	
	def compute(self,T):
		for i,(e,de) in enumerate(zip(self.e,self.de)):
			self.de[i] = (T[i] - self.T) - self.e[i]
			self.e[i] = T[i] - self.T
			self.control_system.input['error'+str(i)] = e
			self.control_system.input['delta'+str(i)] = de
		self.control_system.compute()
		return self.control_system.output['on_off']
		
