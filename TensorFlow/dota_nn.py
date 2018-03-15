import math
import tensorflow as tf
import numpy as np

samples = 10000
batch_size = 8

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def _parse_function(example_proto):
	features = {
		"x" : tf.FixedLenFeature((), tf.string, default_value=""), #name is important should match the name of writing record
		"y": tf.FixedLenFeature((), tf.string, default_value=""),
	}
	#example_proto = tf.Print(example_proto, [example_proto], message="this is example proto: ")
	parsed_features = tf.parse_single_example(example_proto, features)
	#parsed_features['x'] = tf.Print(parsed_features['x'], [parsed_features['x']], message="this is x_raw: ")
	#parsed_features['y'] = tf.Print(parsed_features['y'], [parsed_features['y']], message="this is y: ")
	x_t = tf.decode_raw(parsed_features['x'], tf.float32)
	y_t = tf.decode_raw(parsed_features['y'], tf.float32)
	#tt = x.tensor_content
	#x_t = tf.reshape(x_t, [1,2])
	#x_t = tf.Print(x_t, [x_t.shape], message="this is shape of x: ")
	return {'x' : x_t, 'y' : y_t}

def CreateDataSet(filename):
	d = tf.data.TFRecordDataset(filename)
	d = d.map(_parse_function)
	return d


def model(input):
	x_t = tf.reshape(input, [batch_size, 240])
	W_1 = weight_variable([240, 500])
	W_2 = weight_variable([500, 2])
	W_3 = weight_variable([500, 500])
	b_1 = bias_variable([500])
	b_2 = bias_variable([2])
	b_3 = bias_variable([500])
	layer1 = tf.nn.relu(tf.matmul(x_t, W_1) + b_1)
	layer1_5 = tf.nn.relu(tf.matmul(layer1, W_3) + b_3)
	layer2 = tf.nn.relu(tf.matmul(layer1_5, W_2) + b_2)


	return layer2

def train(filename):
	d = CreateDataSet(filename)
	d = d.batch(batch_size)
	d = d.repeat()
	it = d.make_initializable_iterator()
	n_e = it.get_next()

	x = tf.placeholder(tf.float32)

	y = tf.placeholder(tf.float32)
	y_t = tf.reshape(y, [batch_size, 1])  # important that model dimensions matches label dimensions

	model_out = model(x)
	output = tf.argmax(input=model_out, axis=1)

	one_hot = tf.reshape(tf.one_hot(indices=tf.cast(y_t, tf.int32), depth=2), [batch_size, 2])
	entroy = tf.losses.softmax_cross_entropy(onehot_labels=one_hot, logits=model_out)
	loss = tf.reduce_mean(entroy)

	optimizer = tf.train.GradientDescentOptimizer(0.001)
	train = optimizer.minimize(loss)
	init = tf.global_variables_initializer()

	with tf.Session() as sess:
		sess.run(init)
		sess.run(it.initializer)
		for i in range(100000):#range(int(samples/batch_size)):

			feed = sess.run(n_e)


			feed_dict = { x : feed['x'], y : feed['y']}

			_, _loss, _out, _debug = sess.run([train, loss, model_out, entroy], feed_dict=feed_dict)
			if i % 1000 == 0:
				print("debug1 = {}".format(_debug))
				print("out = {}".format(_out))
				print("total loss = {}".format(_loss))

		accuracy = 0;

		for i in range(1000):#range(int(samples/batch_size)):

			feed = sess.run(n_e)


			feed_dict = { x : feed['x'] }

			a, _b = sess.run([output, model_out], feed_dict=feed_dict)
			for i in range(0,batch_size):
				if a[i] == feed['y'][i,0]:
					accuracy += 1

		print(accuracy)

def test(filename):
	d = CreateDataSet(filename)
	d = d.batch(batch_size)
	d = d.repeat()
	it = d.make_initializable_iterator()
	n_e = it.get_next()

	x = tf.placeholder(tf.float32)

	model_out = model(x)
	output = tf.argmax(input=model_out, axis=1)
	init = tf.global_variables_initializer()
	accuracy = 0
	with tf.Session() as sess:
		sess.run(init)
		sess.run(it.initializer)
		for i in range(1000):#range(int(samples/batch_size)):

			feed = sess.run(n_e)


			feed_dict = { x : feed['x'] }

			a, _b = sess.run([output, model_out], feed_dict=feed_dict)
			for i in range(0,batch_size):
				if a[i] == feed['y'][i,0]:
					accuracy += 1

	print(accuracy)
def main():
	train("ico.tfrecord")



main()
