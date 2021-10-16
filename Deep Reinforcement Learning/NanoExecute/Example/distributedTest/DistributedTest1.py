#%%
import tensorflow as tf 

#%%
dbstrategy = tf.distribute.OneDeviceStrategy(device="/gpu:0")
with dbstrategy.scope():
  model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(1,))])
  model.compile(loss='mse', optimizer='sgd')

#%%
dataset = tf.data.Dataset.from_tensors(([1.], [1.])).repeat(100).batch(10)
model.fit(dataset, epochs=20)
model.evaluate(dataset)
