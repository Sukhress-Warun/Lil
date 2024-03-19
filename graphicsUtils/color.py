import numpy as np
class color_band:
	def __init__(self, cl, loop = False):
		self.unit = 1 / (len(cl) - (1 if (not loop) else 0))
		self.cl = list(map(lambda x : np.array(x), cl))
		self.loop = loop
		self.len = len(cl)
	def getcolor(self, lvl, limit = True):
		if(self.loop and (lvl==0 or lvl==1)):
			return tuple(self.cl[0])
		elif(lvl==1):
			return tuple(self.cl[-1])
		elif(lvl==0):
			return tuple(self.cl[0])
		elif(lvl<0 or lvl>1):
			if not limit:
				raise ValueError("level must be between 0 and 1")
			else:
				lvl = max(0, min(1, lvl))
		t=lvl/self.unit
		ind=int(t)
		rem=t-ind
		dif=(self.cl[(ind+1)%self.len]-self.cl[ind])*(rem)
		return tuple(map(int,tuple(self.cl[ind]+dif)))