import math
import tensorflow as tf
import numpy as np

samples = 10000
batch_size = 4

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
	d = d.batch(batch_size)
	d = d.repeat()
	return d


def pyramid(start_layer, size_start, size_end, step=4):
	size = size_start
	layer = start_layer
	while (size > size_end):
		prev_size = size
		size = size / step
		layer = tf.nn.relu(tf.matmul(layer, weight_variable([int(prev_size), int(size)]))+bias_variable([int(size)]))
	return layer

def model1(input, keep_prob):
	max_size = 1024
	x_t = tf.reshape(input, [batch_size, 240])
	W_1 = weight_variable([240, 512])
	W_2 = weight_variable([512, max_size])
	W_3 = weight_variable([max_size, max_size])
	W_end = weight_variable([128,2])

	b_1 = bias_variable([512])
	b_2 = bias_variable([max_size])
	b_3 = bias_variable([max_size])
	b_end = bias_variable([2])
	layer1 = tf.nn.relu(tf.matmul(x_t, W_1) + b_1)
	layer2 = tf.nn.relu(tf.matmul(layer1, W_2) + b_2)
	layer3 = tf.nn.relu(tf.matmul(layer2, W_3) + b_3)
	layer_next = pyramid(layer2, max_size, 128, step=2)
	drop_out = tf.nn.dropout(layer_next, keep_prob)
	model_out = tf.nn.relu(tf.matmul(drop_out, W_end) + b_end)


	return model_out


def model2(input, keep_prob):
	x_t = tf.reshape(input, [batch_size, 240])
	W_1 = weight_variable([240, 512])
	W_2 = weight_variable([512, 512])
	W_3 = weight_variable([512, 256])
	W_4 = weight_variable([256, 64])
	W_5 = weight_variable([64, 2])
	b_1 = bias_variable([512])
	b_2 = bias_variable([512])
	b_3 = bias_variable([256])
	b_4 = bias_variable([64])
	b_5 = bias_variable([2])
	layer1 = tf.nn.relu(tf.matmul(x_t, W_1) + b_1)
	layer2 = tf.nn.relu(tf.matmul(layer1, W_2) + b_2)
	layer3 = tf.nn.relu(tf.matmul(layer2, W_3) + b_3)
	layer4 = tf.nn.relu(tf.matmul(layer3, W_4) + b_4)
	layer4_5 = tf.nn.dropout(layer4, keep_prob)
	layer5 = tf.nn.relu(tf.matmul(layer4_5, W_5) + b_5)

	return layer5

def train(filename):
	d = CreateDataSet(filename)
	it = d.make_initializable_iterator()
	n_e = it.get_next()

	x = tf.placeholder(tf.float32)

	y = tf.placeholder(tf.float32)
	y_t = tf.reshape(y, [batch_size, 1])  # important that model dimensions matches label dimensions

	model_out = model2(x, keep_prob)
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

		#train loop
		for i in range(100000):#range(int(samples/batch_size)):

			feed = sess.run(n_e)


			feed_dict = { x : feed['x'], y : feed['y'], keep_prob : 0.5}

			_, _loss, _out, _debug = sess.run([train, loss, model_out, entroy], feed_dict=feed_dict)
			if i % 1000 == 0:
				print("debug1 = {}".format(_debug))
				print("out = {}".format(_out))
				print("total loss = {}".format(_loss))

		accuracy = 0;

		for i in range(1000):#range(int(samples/batch_size)):

			feed = sess.run(n_e)


			feed_dict = { x : feed['x'], keep_prob : 1.0 }

			a, _b = sess.run([output, model_out], feed_dict=feed_dict)
			for i in range(0,batch_size):
				if a[i] == feed['y'][i,0]:
					accuracy += 1

		print(accuracy)

def run(train_file, test_file):
	train_ds = CreateDataSet(train_file)
	train_ds_it = train_ds.make_initializable_iterator()
	train_ds_n_e = train_ds_it.get_next()

	test_ds = CreateDataSet(test_file)
	test_ds_it = test_ds.make_initializable_iterator()
	test_ds_n_e = test_ds_it.get_next()

	x = tf.placeholder(tf.float32)

	y = tf.placeholder(tf.float32)
	y_t = tf.reshape(y, [batch_size, 1])  # important that model dimensions matches label dimensions
	keep_prob = tf.placeholder(tf.float32)

	model_out = model2(x, keep_prob)
	prob = tf.nn.softmax(model_out)
	output = tf.argmax(input=model_out, axis=1)

	one_hot = tf.reshape(tf.one_hot(indices=tf.cast(y_t, tf.int32), depth=2), [batch_size, 2])
	entroy = tf.losses.softmax_cross_entropy(onehot_labels=one_hot, logits=model_out)
	loss = tf.reduce_mean(entroy)

	optimizer = tf.train.GradientDescentOptimizer(0.01)
	train = optimizer.minimize(loss)
	init = tf.global_variables_initializer()

	with tf.Session() as sess:
		sess.run(init)
		sess.run(train_ds_it.initializer)

		#train loop
		for i in range(200000):

			feed = sess.run(train_ds_n_e)


			feed_dict = { x : feed['x'], y : feed['y'], keep_prob : 0.5}

			_, _loss, _out, _debug = sess.run([train, loss, model_out, entroy], feed_dict=feed_dict)
			if i % 1000 == 0:

				print("total loss at {} = {}".format(i, _loss))

		#check accuracy of dataset

		accuracy = 0;
		decision = 0;
		sess.run(test_ds_it.initializer)
		for i in range(int(700/batch_size)):#range(int(samples/batch_size)):

			feed = sess.run(test_ds_n_e)


			feed_dict = { x : feed['x'], keep_prob : 1.0 }

			a, _b = sess.run([output, prob], feed_dict=feed_dict)
			for i in range(0,batch_size):
				if _b[i,a[i]] > 0.95:
					decision += 1
					if a[i] == feed['y'][i,0]:
						accuracy += 1

		#check accuracy of just rediant
		acc_temp = 0
		for i in range(int(700/batch_size)):#range(int(samples/batch_size)):





			for i in range(0,batch_size):
				if 1 == feed['y'][i,0]:
					acc_temp += 1

		print(accuracy)
		print(decision)
		print(acc_temp)

def main():
	run("train.tfrecord", "test.tfrecord")



main()
