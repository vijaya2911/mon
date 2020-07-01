from kubernetes import config as kconfig
from kubernetes import client as kclient
import logging
import time

class OdcMonitor():
	def __init__(self, config, logger):
		self.config = config
		self.logger = logger
		self.initKube()

	def initKube(self):
		kconfig.load_incluster_config()
		c=kclient.Configuration()
		c.verify_ssl=False
		kclient.Configuration.set_default(c)
		self.kubeApi=kclient.CoreV1Api()

	def getNamespace(self):
		spaces=self.kubeApi.list_namespace()
		nspaces = []
		for space in spaces.items:
			nspaces.append(space.metadata.name)
		return nspaces

	def getPodInfo(self, nspaces):
		podList = []
		for space in nspaces:
			pods=self.kubeApi.list_namespaced_pod(namespace=space)
			for pod in pods.items:
				podInfo = (pod.metadata.name, pod.metadata.namespace, pod.status.phase)
				podList.append(podInfo)
		return podList

	def getNodeInfo(self):
		nodes=self.kubeApi.list_node()
		nodeList = []
		for node in nodes.items:
			for cond in node.status.conditions:
				if cond.reason == "KubeletReady":
					if cond.status == 'True':
						state = "Ready"
					else:
						state = "Not Ready"
					nodeInfo = (node.metadata.name, state)
					nodeList.append(nodeInfo)
		return nodeList

	def run(self):
		while True:
			self.logger.info("Monitor running ...")
			#nodeList = self.getNodeInfo()
			#self.logger.info(nodeList)
			#nspaces = self.getNamespace()
			#podList = self.getPodInfo(nspaces)
			#self.logger.info(podList)
			time.sleep(config["frequency"])

if __name__ == "__main__":
	config = {"frequency": 60}
	logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
	logger = logging.getLogger("odc-monitor")
	mon = OdcMonitor(config, logger)
	mon.run()
