import tensorflow as tf
import json


class AutoDist(config_file="", address=""):
	"""Automating the distributed configuration and execution"""

	@property
	def session(self):
		return self._session

	@property
	def config(self):
		return self._config

  @property
  def task_index(self):
    return self._task_indexs

  @property
  def is_chief(self):
    return self._is_chief



	__init__(self, config_file, address):
		# create cluster
		### read config_file
		cluster = self._read_config(config_file) 
		self._cluster_spec = tf.train.ClusterSpec(cluster)

		# identifying the current process
		self._address = address
		self._job_name = ""
		self._task_index = ""
		for job in self._cluster_spec.jobs:
			for index, task in self._cluster_spec.job_tasks(job):
				# TODO: should user specify the address of the current process?
				# let's assume that we have that info in variable address
				if task == address:
					self._job_name = job
					self._task_index = index
		
		self._is_chief = self._task_index == 0
		
		self._server = tf.train.Server(self._cluster_spec,
										job_name = self._job_name,
										task_index = self._task_index)
		if(self._job_name == 'worker'):			
			# worker server has more to init
			self._config = tf.ConfigProto(log_device_placement = True)		
			self._session = tf.train.MonitoredTrainingSession(config = config,
															master = server.target,
															is_chief = self._is_chief)


	def _read_config(config_file):
		#for now, config_file has no extra information from the cluster config
		f = open(config_file, 'r')
		data = json.load(f)
		return json.dump(data)



	def device():
		return tf.train.replica_device_setter(
        	worker_device="/job:worker/task:%d" % self._task_index,
        	cluster=self._cluster_spec)


	# This should be called immediately after the class is created
	def start():
		# parameter server calls join, worker server does nothing
		if self._job_name == 'ps':
			self._server.join()
      quit()


