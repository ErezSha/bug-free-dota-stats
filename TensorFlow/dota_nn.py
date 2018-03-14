import math
import tensorflow as tf
import numpy as np

samples = 10000
batch_size = 1

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


def main():
	#sandbox()
	#return
	filename = "ico.tfrecord"
	#WriteToRecordFile(filename)

	#d = tf.data.Dataset.from_tensor_slices({'x' : a, 'y' : l})
	d = CreateDataSet(filename)
	d = d.batch(batch_size)
	d = d.repeat()
	it = d.make_initializable_iterator()
	n_e = it.get_next()



	x = tf.placeholder(tf.float32)
	x_t = tf.reshape(x, [batch_size, 240])

	y = tf.placeholder(tf.float32)
	y_t = tf.reshape(y, [batch_size, 1]) #important that model dimensions matches label dimensions


	W_1 = weight_variable([240, 500])
	W_2 = weight_variable([500, 1])
	W_3 = weight_variable([500, 500])
	b_1 = bias_variable([500])
	b_2 = bias_variable([1])
	b_3 = bias_variable([500])
	layer1 = tf.nn.relu(tf.matmul(x_t, W_1) + b_1)
	layer1_5 = tf.nn.relu(tf.matmul(layer1, W_3) + b_3)
	layer2 = (tf.matmul(layer1_5, W_2) + b_2)
	model_out = layer2 #tf.reshape(layer2, [2, 6])
	#model_out = tf.Print(model_out, [model_out.shape], message="model shape is: ")
	loss = tf.reduce_mean(model_out - y_t)

	optimizer = tf.train.AdamOptimizer(0.2)
	train = optimizer.minimize(loss)
	init = tf.global_variables_initializer()


	with tf.Session() as sess:
		sess.run(init)
		sess.run(it.initializer)
		for i in range(100000):#range(int(samples/batch_size)):

			feed = sess.run(n_e)

			#print(step_x)
			feed_dict = { x : feed['x'], y : feed['y']}
			#print(sess.run(x_t, feed_dict=feed_dict))
			#print(sess.run(y_t, feed_dict=feed_dict))
			a = sess.run(train, feed_dict=feed_dict)
			#print(sess.run(diag0, feed_dict=feed_dict))
			#print(sess.run(area0, feed_dict=feed_dict))
			#print(sess.run(area_ref0, feed_dict=feed_dict))



main()
