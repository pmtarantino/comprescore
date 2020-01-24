import numpy as np

class LogFit():

	def fit(self,x,y):
		return np.polyfit(np.log(x),y,1)

	def predict(self, x, values):
		return values[0] * np.log(x) + values[1]

	def inverse(self, x, values):
		return np.exp((x-values[1])/values[0])