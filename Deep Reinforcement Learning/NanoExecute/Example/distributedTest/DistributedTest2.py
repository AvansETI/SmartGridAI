# imports
from __future__ import absolute_import, division, print_function, unicode_literals
import json, os, socket, sys


import logging
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0' #1 = suppress tf info messages, 2 = supres warnings, 3 = supress all
# loggingFormat = '%(levelname)s\t %(name)s: \t%(message)s'
# logging.basicConfig(format=loggingFormat, level=logging.DEBUG, stream= sys.stdout)
# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
from distributed_network_helper import initDistributedNetwork, getIpsFromArgs
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(logging.DEBUG)

# code om tf als backend goed te laten werken. zonder dit kan er een error komen
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

#get ip's van commandline via een help functie
workerIps, chiefIps, paramServerIps = getIpsFromArgs()
# set tf_config
# alle ip's van de workers. defineer de port erachter waarnaar wordt geluisterd
# first defined is the chief if not else defined
strategy, isMainChief,isChief, isWorker, isParamWorker = initDistributedNetwork(
    workerIps=workerIps, chiefIps=chiefIps, paramServIp=paramServerIps, port=39202)
# define model
#op model voor veel te simpel test data om het wat slomer te laten gaan.
# in een functie gezet zodat deze op het juiste moment aangeroepen kan worden
def build_and_compile_cnn_model():
  model = tf.keras.Sequential([
      tf.keras.layers.Dense(1, input_shape=(1,)),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(64, activation='relu'),
      tf.keras.layers.Dense(64, activation='relu'),
      tf.keras.layers.Dense(10, activation='softmax')])
  model.compile(
      loss=tf.keras.losses.sparse_categorical_crossentropy,
      optimizer=tf.keras.optimizers.SGD(learning_rate=0.001),
      metrics=['accuracy'])
  return model

# #%% test if the model worsk localy zonder distributed
# single_worker_model = build_and_compile_cnn_model()
# single_worker_model.fit(x=train_datasets, epochs=3)


NUM_WORKERS = len(workerIps)#workerArray.count
# strategy = tf.distribute.OneDeviceStrategy(device="/gpu:0")
# NUM_WORKERS = 1

#
# Here the batch size scales up by number of workers since 
# `tf.data.Dataset.batch` expects the global batch size. Previously we used 64, 
# and now this becomes 128.
WORKER_BATCH_SIZE = 128
GLOBAL_BATCH_SIZE = WORKER_BATCH_SIZE * NUM_WORKERS


# alles in deze scope wordt gesynced.
with strategy.scope():  
  # Creation of dataset, and model building/compiling need to be within 
  # `strategy.scope()`.
  # build training set
  train_datasets = tf.data.Dataset\
      .from_tensors(([1.], [1.]))\
      .repeat(GLOBAL_BATCH_SIZE * 2)\
      .batch(GLOBAL_BATCH_SIZE)\
      .shuffle(buffer_size=1000)

  # turn off outo sharding
  # options = tf.data.Options() 
  # options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.OFF
  # train_datasets_no_auto_shard = train_datasets.with_options(options)



  multi_worker_model = build_and_compile_cnn_model()# model building en compileren  in strategy scope

callbacks = [tf.keras.callbacks.ModelCheckpoint(filepath='/tmp/keras-ckpt')]
# start met trainen
print("start training")
multi_worker_model.fit(x=train_datasets, epochs=30, callbacks= callbacks)
print("ended")
# K.clear_session()
try:
  exit()
# except UnimplementedError as i:
#   logging.info(i)
#   pass
except AttributeError as identifier:
  print("exit error: "+ identifier)
  pass


