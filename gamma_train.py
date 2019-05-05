"""-*- coding: utf-8 -*-
 DateTime   : 2019/5/5 10:25
 Author  : Peter_Bonnie
 FileName    : gamma_train.py
 Software: PyCharm
"""
import tensorflow as tf
from keras import backend as K
import numpy as np
import h5py
from tensorflow.python.framework import ops
ops.reset_default_graph()
sess=tf.Session()

#主要用于获取最佳的gamma值
def get_gamma_value(sess,input1,input2,input3):

    """use nn to search the best gamma value

    Args:
        input1(file):predict value on LSTM+ATTN model
        input2(file):predict value on LSTM model
        input3(file):real value

        algorithm:
             predict=(inputs-inputs)*gamma+inputs
             loss=predict-inputs
    Returns:
         the best gamma value

    """
    #load dataset
    pass


input1=np.loadtxt("LSTM-ATTN-predict.txt")
input2=np.loadtxt("LSTM-predict.txt")
input3=np.loadtxt("real.txt")

errors=np.array([i-j for i,j in zip(input1,input2)])


#define model
with tf.name_scope("X_Y"):
    error=tf.placeholder(dtype=tf.float32,shape=[None,1],name='error')
    X=tf.placeholder(dtype=tf.float32,shape=[None,1],name='x')
    Y=tf.placeholder(dtype=tf.float32,shape=[None,1],name='y')
    gamma=tf.Variable(initial_value=tf.random_normal(shape=[1,1],stddev=1.0,dtype=tf.float32),trainable=True)
    model_output=tf.add(tf.matmul(error,gamma),X)

    # with tf.name_scope("loss function"):
        # loss=tf.reduce_mean(tf.square(Y,model_output))
loss=tf.losses.mean_squared_error(Y,model_output)
init=tf.global_variables_initializer()
sess.run(init)
with tf.name_scope('opt'):
    optimizer=tf.train.GradientDescentOptimizer(learning_rate=0.01)
    train_step=optimizer.minimize(loss)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(20):
        #进行50轮训练
        # rand_idx=np.random.choice(len(errors),size=2)
        rand_idx=[i for i in range((i+1)*5)]
        rand_err=np.transpose([errors[rand_idx]])
        rand_y=np.transpose([input3[:,-1][rand_idx]])
        rand_x=np.transpose([input2[rand_idx]])
        sess.run(train_step,feed_dict={error:rand_err,X:rand_x,Y:rand_y})
        my_loss,final_output=sess.run([loss,model_output],feed_dict={error:rand_err,X:rand_x,Y:rand_y})
        print("loss:{0},gamma:{1}.".format(my_loss,sess.run(gamma)))


# #mian func
# def main():
#     get_gamma_value(sess,"LSTM-ATTN-predict.txt","LSTM-predict.txt","real.txt")
#
# if __name__=='__main__':
#
#     tf.app.run(main=main())




