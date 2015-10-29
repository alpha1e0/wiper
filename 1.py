
import time
from multiprocessing import Process, Manager

print "start"

class cl(object):
	def __init__(self,des):
		self.des = des
	def show(self):
		print self.des


class Plugin(Process):
	def bind(self, inchannel, outchannel=None):
		self.inchannel = inchannel
		self.outchannel = outchannel
	def get(self):
		return self.inchannel.pop()
	def put(self, data):
		self.outchannel.append(data)

	def run(self):
		print "process:", self.name
		for i in xrange(1,5):
			try:
				print self.name + "getting"
				data = self.get()
				#print self.inchannel
			except IndexError:
				continue
			except AttributeError:
				break
			else:
				#print self.name
				print self.name + " got " + data.des
				data.des = self.name + " handle"
				if self.outchannel is not None:
					self.put(data)
			finally:
				time.sleep(2)


aa = Plugin()
bb = Plugin()
init = cl("init")

mgr = Manager()
l1 = mgr.list()
l2 = mgr.list()

aa.bind(l1,l2)
bb.bind(l2)
#bb.bind(l1)


l1.append(init)

aa.start()
bb.start()

time.sleep(10)



