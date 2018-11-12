from sklearn.linear_model import LinearRegression
from statistics import mean

class MML:

	def __init__(self, windowSize):
		self._data = {
			'xaxis' : [],
			'yaxis' : []
		}

		self._window_data = []
		self._window_size = windowSize

	def getValueNow(self):
		return (self._data['xaxis'][-1], self._data['yaxis'][-1])

	def push(self, values):
		self._window_data.append(values[1])

		if len(self._window_data) > self._window_size:
			self._window_data = self._window_data[-self._window_size:]

		self._data['xaxis'].append(values[0])
		self._data['yaxis'].append(mean(self._window_data))

	def setWindowSize(self, size):
		self._window_size = size

	def getDataArray(self):
		return self._data


