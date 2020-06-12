import tensorflow as tf
import numpy
import matplotlib.pyplot as plt

learning_rates = []
initial_rate = 100.0
step_to_decay = 1
decay_rate = 0.8

with tf.Session() as sess:
  global_step = tf.placeholder(tf.int32, shape=[])
  learning_rate = tf.train.exponential_decay(initial_rate, global_step, step_to_decay, decay_rate)
  tf.global_variables_initalizer().run()

  for step in range(training_steps):
    learning_rate.append(learning_rate.eval(feed_dict={global_step: step}))

fig, ax1 = plt.subplot(1, 1)
fig.set_size_inches(10, 4)
ax1.plot(range(0, training_steps), learning_rates)
plt.show()