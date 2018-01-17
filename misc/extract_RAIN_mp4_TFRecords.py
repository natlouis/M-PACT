import os
import time
import argparse
import tensorflow      as tf
import numpy           as np
import multiprocessing as mp


import matplotlib.pyplot as plt
import matplotlib.animation as animation


from tensorflow.python.ops      import clip_ops
from tensorflow.python.ops      import init_ops
from tensorflow.python.ops      import control_flow_ops
from tensorflow.python.ops      import variable_scope as vs
from tensorflow.python.ops      import variables as vars_
from tensorflow.python.training import queue_runner_impl


from utils                                            import *
from Queue                                            import Queue
from models                                           import *
from logger                                           import Logger
from random                                           import shuffle
from load_dataset_tfrecords                           import load_dataset
#
# from models.resnet_RIL.resnet_RIL_interp_mean_model_v1  import ResNet_RIL_Interp_Mean_v1
# from models.resnet_RIL.resnet_RIL_interp_mean_model_v2  import ResNet_RIL_Interp_Mean_v2
# from models.resnet_RIL.resnet_RIL_interp_mean_model_v3  import ResNet_RIL_Interp_Mean_v3
# from models.resnet_RIL.resnet_RIL_interp_mean_nosort_v4 import ResNet_RIL_Interp_Mean_Nosort_v4
# from models.resnet_RIL.resnet_RIL_interp_mean_model_v8  import ResNet_RIL_Interp_Mean_v8
# from models.resnet_RIL.resnet_RIL_interp_mean_model_v10 import ResNet_RIL_Interp_Mean_v10
# from models.resnet_RIL.resnet_RIL_interp_mean_model_v11 import ResNet_RIL_Interp_Mean_v11
# from models.resnet_RIL.resnet_RIL_interp_mean_model_v18 import ResNet_RIL_Interp_Mean_v18
#
# from models.resnet_RIL.resnet_RIL_interp_median_model_v1  import ResNet_RIL_Interp_Median_v1
# from models.resnet_RIL.resnet_RIL_interp_median_model_v2  import ResNet_RIL_Interp_Median_v2
# from models.resnet_RIL.resnet_RIL_interp_median_model_v3  import ResNet_RIL_Interp_Median_v3
# from models.resnet_RIL.resnet_RIL_interp_median_nosort_v4 import ResNet_RIL_Interp_Median_Nosort_v4
# from models.resnet_RIL.resnet_RIL_interp_median_model_v6  import ResNet_RIL_Interp_Median_v6
# from models.resnet_RIL.resnet_RIL_interp_median_model_v6_1  import ResNet_RIL_Interp_Median_v6_1
# from models.resnet_RIL.resnet_RIL_interp_median_model_v8  import ResNet_RIL_Interp_Median_v8
# from models.resnet_RIL.resnet_RIL_interp_median_model_v10 import ResNet_RIL_Interp_Median_v10
# from models.resnet_RIL.resnet_RIL_interp_median_model_v11 import ResNet_RIL_Interp_Median_v11
# from models.resnet_RIL.resnet_RIL_interp_median_model_v12 import ResNet_RIL_Interp_Median_v12
# from models.resnet_RIL.resnet_RIL_interp_median_model_v12_1 import ResNet_RIL_Interp_Median_v12_1
# from models.resnet_RIL.resnet_RIL_interp_median_model_v14 import ResNet_RIL_Interp_Median_v14
# from models.resnet_RIL.resnet_RIL_interp_median_model_v14_1 import ResNet_RIL_Interp_Median_v14_1
# from models.resnet_RIL.resnet_RIL_interp_median_model_v14_2 import ResNet_RIL_Interp_Median_v14_2
# from models.resnet_RIL.resnet_RIL_interp_median_model_v14_3 import ResNet_RIL_Interp_Median_v14_3
# from models.resnet_RIL.resnet_RIL_interp_median_model_v15 import ResNet_RIL_Interp_Median_v15
# from models.resnet_RIL.resnet_RIL_interp_median_model_v16 import ResNet_RIL_Interp_Median_v16
# from models.resnet_RIL.resnet_RIL_interp_median_model_v17 import ResNet_RIL_Interp_Median_v17
# from models.resnet_RIL.resnet_RIL_interp_median_model_v18 import ResNet_RIL_Interp_Median_v18
# from models.resnet_RIL.resnet_RIL_interp_median_model_v19 import ResNet_RIL_Interp_Median_v19
# from models.resnet_RIL.resnet_RIL_interp_median_model_v21 import ResNet_RIL_Interp_Median_v21
# from models.resnet_RIL.resnet_RIL_interp_median_model_v22 import ResNet_RIL_Interp_Median_v22
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23 import ResNet_RIL_Interp_Median_v23
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23_lstm import ResNet_RIL_Interp_Median_v23_lstm
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23_1 import ResNet_RIL_Interp_Median_v23_1
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23_1_1 import ResNet_RIL_Interp_Median_v23_1_1
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23_2 import ResNet_RIL_Interp_Median_v23_2
from models.resnet_RIL.resnet_RIL_interp_median_model_v23_2_1 import ResNet_RIL_Interp_Median_v23_2_1
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23_2_1_lstm import ResNet_RIL_Interp_Median_v23_2_1_lstm
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23_2_2 import ResNet_RIL_Interp_Median_v23_2_2
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23_3 import ResNet_RIL_Interp_Median_v23_3
from models.resnet_RIL.resnet_RIL_interp_median_model_v23_4 import ResNet_RIL_Interp_Median_v23_4
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23_4_lstm import ResNet_RIL_Interp_Median_v23_4_lstm
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23_5 import ResNet_RIL_Interp_Median_v23_5
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23_6 import ResNet_RIL_Interp_Median_v23_6
from models.resnet_RIL.resnet_RIL_interp_median_model_v23_7_1 import ResNet_RIL_Interp_Median_v23_7_1
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23_7_2 import ResNet_RIL_Interp_Median_v23_7_2
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23_8_1 import ResNet_RIL_Interp_Median_v23_8_1
# from models.resnet_RIL.resnet_RIL_interp_median_model_v23_8_2 import ResNet_RIL_Interp_Median_v23_8_2
# from models.resnet_RIL.resnet_RIL_interp_median_model_v24 import ResNet_RIL_Interp_Median_v24
# from models.resnet_RIL.resnet_RIL_interp_median_model_v24_1 import ResNet_RIL_Interp_Median_v24_1
# from models.resnet_RIL.resnet_RIL_interp_median_model_v24_lstm import ResNet_RIL_Interp_Median_v24_lstm
# from models.resnet_RIL.resnet_RIL_interp_median_model_v25 import ResNet_RIL_Interp_Median_v25
# from models.resnet_RIL.resnet_RIL_interp_median_model_v26 import ResNet_RIL_Interp_Median_v26
# from models.resnet_RIL.resnet_RIL_interp_median_model_v26_1 import ResNet_RIL_Interp_Median_v26_1
# from models.resnet_RIL.resnet_RIL_interp_median_model_v26_2 import ResNet_RIL_Interp_Median_v26_2
# from models.resnet_RIL.resnet_RIL_interp_median_model_v26_3 import ResNet_RIL_Interp_Median_v26_3
# from models.resnet_RIL.resnet_RIL_interp_median_model_v27 import ResNet_RIL_Interp_Median_v27
# from models.resnet_RIL.resnet_RIL_interp_median_model_v28 import ResNet_RIL_Interp_Median_v28
# from models.resnet_RIL.resnet_RIL_interp_median_model_v29 import ResNet_RIL_Interp_Median_v29
# from models.resnet_RIL.resnet_RIL_interp_median_model_v30 import ResNet_RIL_Interp_Median_v30
# from models.resnet_RIL.resnet_RIL_interp_median_model_v31 import ResNet_RIL_Interp_Median_v31
# from models.resnet_RIL.resnet_RIL_interp_median_model_v31_1 import ResNet_RIL_Interp_Median_v31_1
# from models.resnet_RIL.resnet_RIL_interp_median_model_v31_2 import ResNet_RIL_Interp_Median_v31_2
from models.resnet_RIL.resnet_RIL_interp_median_model_v31_3 import ResNet_RIL_Interp_Median_v31_3
# from models.resnet_RIL.resnet_RIL_interp_median_model_v31_3_lstm import ResNet_RIL_Interp_Median_v31_3_lstm
# from models.resnet_RIL.resnet_RIL_interp_median_model_v32 import ResNet_RIL_Interp_Median_v32
# from models.resnet_RIL.resnet_RIL_interp_median_model_v33 import ResNet_RIL_Interp_Median_v33
# from models.resnet_RIL.resnet_RIL_interp_median_model_v34 import ResNet_RIL_Interp_Median_v34
# from models.resnet_RIL.resnet_RIL_interp_median_model_v34_1 import ResNet_RIL_Interp_Median_v34_1
# from models.resnet_RIL.resnet_RIL_interp_median_model_v34_2 import ResNet_RIL_Interp_Median_v34_2
# from models.resnet_RIL.resnet_RIL_interp_median_model_v34_3 import ResNet_RIL_Interp_Median_v34_3
from models.resnet_RIL.resnet_RIL_interp_median_model_v34_3_lstm import ResNet_RIL_Interp_Median_v34_3_lstm

# from models.resnet_RIL.resnet_RIL_interp_max_model_v1  import ResNet_RIL_Interp_Max_v1
# from models.resnet_RIL.resnet_RIL_interp_max_model_v2  import ResNet_RIL_Interp_Max_v2
# from models.resnet_RIL.resnet_RIL_interp_max_model_v3  import ResNet_RIL_Interp_Max_v3
# from models.resnet_RIL.resnet_RIL_interp_max_nosort_v4 import ResNet_RIL_Interp_Max_Nosort_v4
# from models.resnet_RIL.resnet_RIL_interp_max_model_v8  import ResNet_RIL_Interp_Max_v8
# from models.resnet_RIL.resnet_RIL_interp_max_model_v10 import ResNet_RIL_Interp_Max_v10
# from models.resnet_RIL.resnet_RIL_interp_max_model_v20 import ResNet_RIL_Interp_Max_v20

_R_MEAN = 123.68
_G_MEAN = 116.78
_B_MEAN = 103.94

def _average_gradients(tower_grads):
    """
    Calculate the average gradient for each shared variable across all towers.
    Note that this function provides a synchronization point across all towers.
    Args:
        tower_grads: List of lists of (gradient, variable) tuples. The outer list
                     is over individual gradients. The inner list is over the gradient
                     calculation for each tower.
    Returns:
        List of pairs of (gradient, variable) where the gradient has been averaged
        across all towers.
    """

    average_grads = []

    for grad_and_vars in zip(*tower_grads):
        # Note that each grad_and_vars looks like the following:
        #   ((grad0_gpu0, var0_gpu0), ... , (grad0_gpuN, var0_gpuN))
        grads = []

        for g, _ in grad_and_vars:
            # Add 0 dimension to the gradients to represent the tower.
            expanded_g = tf.expand_dims(g, 0)

            # Append on a 'tower' dimension which we will average over below.
            grads.append(expanded_g)

        # END FOR

        # Average over the 'tower' dimension.
        grad = tf.concat(axis=0, values=grads)
        grad = tf.reduce_mean(grad, 0)

        # Keep in mind that the Variables are redundant because they are shared
        # across towers. So .. we will just return the first tower's pointer to
        # the Variable.
        v = grad_and_vars[0][1]
        grad_and_var = (grad, v)
        average_grads.append(grad_and_var)

    # END FOR

    return average_grads


#def _validate(model, sess, experiment_name, logger, dataset, input_dims, output_dims, split, gs, size, k, base_data_path, seq_length, num_vids, wd=0.0):
#    """
#    Args:
#        :model:                  tf-activity-recognition framework model object
#        :sess:                   Tensorflow session object
#        :experiment_name:        Name of current experiment
#        :logger:                 Logger class object
#        :dataset:                Name of dataset being processed
#        :input_dims:             Number of frames used in input
#        :output_dims:            Integer number of classes in current dataset
#        :split:                  Split of dataset being used
#        :gs:                     Integer for global step count
#        :size:                   List detailing height and width of frame
#        :x_placeholder:          Tensorflow placeholder for input frames
#        :istraining_placeholder: Tensorflow placeholder for boolean indicating phase (TRAIN OR TEST)
#        :j_placeholder:          Tensorflow placeholder for number of disjoing sets from application of a sliding window
#        :K:                      Temporal width of sliding window
#        :base_data_path:         Full path to root directory containing datasets
#        :seq_length:             Length of output sequence expected from LSTM
#
#    """
#
#    if 'HMDB51' in dataset:
#        f_name = 'testlist'
#
#    else:
#        f_name = 'testlist'
#
#    # END IF
#
#    istraining = False
#    j          = [input_dims / k]
#    data_path  = os.path.join(base_data_path, 'tfrecords_'+dataset, 'Split'+str(split), f_name)
#
#    # Setting up tensors for models
#    input_data_tensor, labels_tensor, names_tensor = load_dataset(model, 1, output_dims, input_dims, size, data_path, dataset, istraining)
#
#    logits = model.inference(input_data_tensor[0,:,:,:,:],
#                             istraining,
#                             input_dims,
#                             output_dims,
#                             seq_length,
#                             'tower_0', k, j,
#                             weight_decay=wd)
#
#    batch_count = 0
#    acc         = 0
#
#    fin = False
#
#    for vid_num in range(num_vids):
#        batch_count+=1
#        predictions = sess.run(logits)
#
#        # For ResNet and VGG16 based setup only : Need to add support for LRCN multi-GPU validation
#        # ------------------------------------------------
#
#        for pred_idx in range(len(predictions)):
#            guess = np.mean(predictions[pred_idx], 0).argmax()
#
#            if int(pred) == int(labels[pred_idx][0]):
#                acc+=1
#
#            # END IF
#
#        # END FOR
#        # --------------------------------------------------
#
#        logger.add_scalar_value('val/step_acc',acc/float(batch_count), step=batch_count)
#
#    # END FOR
#
#    coord.request_stop()
#    coord.join(threads)
#
#    logger.add_scalar_value('val/acc',acc/float(batch_countcount), step=gs)


def train(model, input_dims, output_dims, seq_length, size, num_gpus, dataset, experiment_name, load_model, num_vids, val_num_vids, n_epochs, split, base_data_path, f_name, learning_rate_init, wd, save_freq, val_freq, k=25):

    """
    Args:
        :model:              tf-activity-recognition framework model object
        :input_dims:         Number of frames used in input
        :output_dims:        Integer number of classes in current dataset
        :seq_length:         Length of output sequence expected from LSTM
        :size:               List detailing height and width of frame
        :num_gpus:           Number of gpus to use when training
        :dataset:            Name of dataset being processed
        :experiment_name:    Name of current experiment
        :load_model:         Boolean variable indicating whether to load form a checkpoint or not
        :num_vids:           Number of videos to be used for training
        :val_num_vids:       Number of videos to be used for validation/testing
        :n_epochs:           Total number of epochs to train
        :split:              Split of dataset being used
        :base_data_path:     Full path to root directory containing datasets
        :f_name:             Prefix for HDF5 to be used
        :learning_rate_init: Initializer for learning rate
        :wd:                 Weight decay
        :save_freq:          Frequency, in epochs, with which to save
        :val_freq:           Frequency, in epochs, with which to run validaton
        :k:                  Width of temporal sliding window

    """

    with tf.name_scope("my_scope") as scope:
        global_step     = tf.Variable(0, name='global_step', trainable=False)
        istraining      = True
        reuse_variables = None
        j               = input_dims / k

        data_path = os.path.join(base_data_path, 'tfrecords_'+dataset, 'Split'+str(split), f_name)

        # Setting up tensors for models
        input_data_tensor, labels_tensor, names_tensor = load_dataset(model, num_gpus, output_dims, input_dims, seq_length, size, data_path, dataset, istraining)

        tower_losses  = []
        tower_grads   = []
        tower_slogits = []

        # Define optimizer
        optimizer = lambda lr: tf.train.MomentumOptimizer(learning_rate=lr, momentum=0.9)

        for gpu_idx in range(num_gpus):
            with tf.device('/gpu:'+str(gpu_idx)):
                with tf.name_scope('%s_%d' % ('tower', gpu_idx)) as scope:
                    with tf.variable_scope(tf.get_variable_scope(), reuse = reuse_variables):
                        logits = model.inference(input_data_tensor[gpu_idx,:,:,:,:],
                                                 istraining,
                                                 input_dims,
                                                 output_dims,
                                                 seq_length,
                                                 scope, k, j,
                                                 weight_decay=wd)

                        # Calculating Softmax for probability outcomes : Can be modified
                        # Make function internal to model
                        slogits = tf.nn.softmax(logits)

                        # Why retain learning rate here ?
                        lr = vs.get_variable("learning_rate", [],trainable=False,initializer=init_ops.constant_initializer(learning_rate_init))

                    # END WITH

                    reuse_variables = True

                    """ Within GPU mini-batch: 1) Calculate loss,
                                               2) Initialize optimizer with required learning rate and
                                               3) Compute gradients
                                               4) Aggregate losses, gradients and logits
                    """
                    total_loss = model.loss(logits, labels_tensor[gpu_idx, :])
                    opt        = optimizer(lr)
                    gradients  = opt.compute_gradients(total_loss, vars_.trainable_variables())

                    tower_losses.append(total_loss)
                    tower_grads.append(gradients)
                    tower_slogits.append(slogits)

            # END WITH

        # END FOR

        """  After: 1) Computing gradients and losses need to be stored and averaged
                    2) Clip gradients by norm to required value
                    3) Apply mean gradient updates
        """

        gradients            = _average_gradients(tower_grads)
        gradients, variables = zip(*gradients)
        clipped_gradients, _ = clip_ops.clip_by_global_norm(gradients, 5.0)
        gradients            = list(zip(clipped_gradients, variables))
        grad_updates         = opt.apply_gradients(gradients, global_step=global_step, name="train")
        train_op             = grad_updates


        # Logging setup initialization
        log_name     = ("exp_train_%s_%s_%s" % ( time.strftime("%d_%m_%H_%M_%S"),
                                                           dataset,
                                                           experiment_name))
        make_dir(os.path.join('results',model.name))
        make_dir(os.path.join('results',model.name, dataset))
        make_dir(os.path.join('results',model.name, dataset, experiment_name))
        make_dir(os.path.join('results',model.name, dataset, experiment_name, 'checkpoints'))
        curr_logger = Logger(os.path.join('logs',model.name,dataset, log_name))

        # TF session setup
        config  = tf.ConfigProto(allow_soft_placement=True)
        sess    = tf.Session(config=config)
        saver   = tf.train.Saver()
        init    = tf.global_variables_initializer()
        coord   = tf.train.Coordinator()
        threads = queue_runner_impl.start_queue_runners(sess=sess, coord=coord)

        sess.run(init)

        if load_model:
            ckpt = tf.train.get_checkpoint_state(os.path.dirname(os.path.join('results', model.name, dataset,  experiment_name, 'checkpoints/checkpoint')))
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
                print 'A better checkpoint is found. Its global_step value is: ', global_step.eval(session=sess)

            else:
                print "Failed loading checkpoint requested. Please check."
                exit()

            # END IF

        # END IF


        epoch_count    = 0
        acc            = 0
        tot_train_time = 0.0
        tot_load_time  = 0.0

        losses     = []
        total_pred = []
        save_data  = []

        lr = learning_rate_init

        # Timing test setup
        time_init = time.time()

        for tot_count in range(0, n_epochs*num_vids, num_gpus):

            # Variable to update during epoch intervals
            for gpu_idx in range(num_gpus):
                if tot_count%num_vids == gpu_idx:
                    batch_count = 0
                    epoch_acc   = 0

                    if epoch_count%save_freq == 0:# and tot_count > 0:
                        print "Saving..."
                        saver.save(sess, os.path.join('results', model.name, dataset, experiment_name,'checkpoints/checkpoint'), global_step.eval(session=sess))

                    # END IF

                    epoch_count += 1



            time_pre_train = time.time()

            _, loss_train, predictions, gs, labels = sess.run([train_op, tower_losses,
                                                                           tower_slogits, global_step,
                                                                           labels_tensor])


            for pred_idx in range(len(predictions)):
                pred = np.mean(predictions[pred_idx], 0).argmax()

                if pred == labels[pred_idx][0]:
                    epoch_acc +=1

                # END IF

                batch_count+=1

            # END FOR

            time_post_train = time.time()
            tot_train_time += time_post_train - time_pre_train


            print 'train_time: ', time_post_train-time_pre_train
            print 'step, loss: ', gs, loss_train

            curr_logger.add_scalar_value('train/train_time',time_post_train - time_pre_train, step=gs)
            curr_logger.add_scalar_value('train/loss',      float(np.mean(loss_train)), step=gs)

            curr_logger.add_scalar_value('train/epoch_acc', epoch_acc/float(batch_count), step=gs)


            # END IF

            #if int(tot_count/num_vids) % val_freq == 0:
            #    _validate(model, sess, experiment_name, curr_logger, dataset, input_dims, output_dims, split, gs, size, k, base_data_path, seq_length, val_num_vids)
            #
            ## END IF

        print "Saving..."
        saver.save(sess, os.path.join('results', model.name, dataset, experiment_name,'checkpoints/checkpoint'), global_step.eval(session=sess))

        coord.request_stop()
        coord.join(threads)


        print "Tot train time: ", tot_train_time
        print "Tot time:       ", time.time()-time_init



def _clip_logits(model, input_data_tensor, istraining, input_dims, output_dims, seq_length, scope, k, j):
    #import pdb; pdb.set_trace()
    # Model Inference
    logits_list = tf.map_fn(lambda clip_tensor: model.inference(clip_tensor,
                             istraining,
                             input_dims,
                             output_dims,
                             seq_length,
                             scope,), input_data_tensor[0,:,:,:,:,:])
    #import pdb; pdb.set_trace()
    # Logits
    softmax = tf.map_fn(lambda logits: tf.nn.softmax(logits), logits_list)

    return logits_list, softmax

def _video_logits(model, input_data_tensor, istraining, input_dims, output_dims, seq_length, scope, k, j, dataset):


    if "RIL" in model.name:
        # Model Inference
        logits = model.inference(input_data_tensor[0,:,:,:,:],
                                 istraining,
                                 input_dims,
                                 output_dims,
                                 seq_length,
                                 scope,
                                # return_layer = "RIlayer")
                                # return_layer = "RAINlayer")
                                 return_layer = ['Parameterization_Variables', 'Parameterization_Variables_phi'])
                                # return_layer = 'Parameterization_Variable_Phi')
                                # return_layer = 'Parameterization_Variable_Alpha')
                                # return_layer = 'RAINlayer_lstm_fc_4')
    else:
        # Model Inference
        logits = model.inference(input_data_tensor[0,:,:,:,:],
                                 istraining,
                                 input_dims,
                                 output_dims,
                                 seq_length,
                                 scope, k, j)
    # Logits
    #softmax = tf.nn.softmax(logits)
    softmax = logits
    return logits, softmax

def save_gif(frames, name, model, dataset, vid_num):
    my_dpi = 16
    #frames = frames[...,::-1]
    #fig, ax = plt.subplots()
    fig = plt.figure(figsize=(224/my_dpi*2,224/my_dpi*2), dpi=my_dpi)

    ax = fig.add_subplot(111)
    #fig.subplots_adjust(left=0, bottom=0, right=0, top=0, wspace=None, hspace=None)
    #ax.axis('tight')
    ax.axis('off')
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    #ax.set_frame_on(False)
    #ax.set_axis_off()
    #fig.set_size_inches(14,14,forward=True)
    #import pdb; pdb.set_trace()
    def animate(i):
        if i < frames.shape[0]:
            frame = np.zeros((224,224,3))
            frame[:,:,0] = frames[i][:,:,0] + _R_MEAN
            frame[:,:,1] = frames[i][:,:,1] + _G_MEAN
            frame[:,:,2] = frames[i][:,:,2] + _B_MEAN
            return ax.imshow(frame/255.0, aspect='auto')
        else:
            frame = np.zeros((224,224,3))
            return ax.imshow(frame/255.0, aspect='auto')
    ims = map(lambda x: (animate(x), ax.set_title('')), range(frames.shape[0]+25))
    anim = animation.ArtistAnimation(fig, ims, interval=frames.shape[0]+25,)
    #plt.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
    #fig.set_tight_layout(True)
#    plt.show()
    make_dir(os.path.join('results/gifs', dataset.split('Rate')[0]+'_'+model.name))
    make_dir(os.path.join('results/gifs', dataset.split('Rate')[0]+'_'+model.name, vid_num))
    anim.save(os.path.join('results/gifs', dataset.split('Rate')[0]+'_'+model.name,vid_num,name+'.mp4'), writer='imagemagick', fps=25, dpi=my_dpi)
    print "Saved ", name
    plt.cla()
    plt.clf()
    plt.close(fig)
    #import pdb;pdb.set_trace()
#    for frame in frames:





def test(model, input_dims, output_dims, seq_length, size, dataset, loaded_dataset, experiment_name, num_vids, split, base_data_path, f_name, load_model, k=25, extract_end=0, verbose=0):

    """
    Function used to test the performance and analyse a chosen model
    Args:
        :model:              tf-activity-recognition framework model object
        :input_dims:         Number of frames used in input
        :output_dims:        Integer number of classes in current dataset
        :seq_length:         Length of output sequence expected from LSTM
        :size:               List detailing height and width of frame
        :dataset:            Name of dataset being loaded
        :loaded_dataset:     Name of dataset which was used to train the current model
        :experiment_name:    Name of current experiment
        :num_vids:           Number of videos to be used for training
        :split:              Split of dataset being used
        :base_data_path:     Full path to root directory containing datasets
        :f_name:             Specific video directory within a chosen split of a dataset
        :k:                  Width of temporal sliding window
        :verbose:            Boolean to indicate if all print statement should be procesed or not

    Returns:
        Does not return anything
    """

    with tf.name_scope("my_scope") as scope:

        # Initializers for checkpoint and global step variable
        ckpt    = None
        gs_init = 0
        j           = input_dims / k
        # Load pre-trained/saved model
        if load_model:
            try:
                ckpt, gs_init, learning_rate_init = load_checkpoint(model.name, loaded_dataset, experiment_name)
                if verbose:
                    print 'A better checkpoint is found. Its global_step value is: ' + str(gs_init)

            except:
                if verbose:
                    print "Failed loading checkpoint requested. Please check."
                exit()

            # END TRY
        else:
            ckpt = model.load_default_weights()

        # END IF

        # Initialize model variables
        istraining  = False
        global_step = tf.Variable(gs_init, name='global_step', trainable=False)

        data_path   = os.path.join(base_data_path, 'tfrecords_'+dataset, 'Split'+str(split), f_name)

        # Setting up tensors for models
        input_data_tensor, labels_tensor, names_tensor = load_dataset(model, 1, output_dims, input_dims, seq_length, size, data_path, dataset, istraining)

        if len(input_data_tensor.shape) > 5:
            logits, softmax = _clip_logits(model, input_data_tensor, istraining, input_dims, output_dims, seq_length, scope, k, j)
        else:
            logits, softmax = _video_logits(model, input_data_tensor, istraining, input_dims, output_dims, seq_length, scope, k, j, dataset)

        # END IF

        # Logger setup (Name format: Date, month, hour, minute and second, with a prefix of exp_test)
        log_name    = ("exp_test_%s_%s_%s" % ( time.strftime("%d_%m_%H_%M_%S"),
                                               dataset, experiment_name))
        curr_logger = Logger(os.path.join('logs',model.name,dataset, log_name))

        # TF session setup
        sess    = tf.Session()
        init    = (tf.global_variables_initializer(), tf.local_variables_initializer())
        coord   = tf.train.Coordinator()
        threads = queue_runner_impl.start_queue_runners(sess=sess, coord=coord)

        # Variables get randomly initialized into tf graph
        sess.run(init)

        # Model variables initialized from previous saved models
        initialize_from_dict(sess, ckpt)
        del ckpt

        acc        = 0
        count      = 0
        total_pred = []



        print "Begin Testing"

        if 'Rate' in dataset:
            rate_label = 'Rate'
        else:
            rate_label = 'Orig'
        if 'RIL' in model.name:
            model_label = 'RIL'
        else:
            model_label = 'res'

        for vid_num in range(50):
            count +=1
            if extract_end:
                d1 = tf.get_default_graph().get_tensor_by_name('my_scope/sub_3:0')
                d2 = tf.get_default_graph().get_tensor_by_name('my_scope/sub_4:0')
                output_idx = tf.get_default_graph().get_tensor_by_name('my_scope/clip_by_value:0')
                input_data, labels, names, d1, d2, output_idx = sess.run([input_data_tensor, labels_tensor, names_tensor, d1, d2, output_idx])
                #frames = frames[0]
            #    import pdb; pdb.set_trace()
                input_data = input_data[0]

                d1 = np.reshape(np.tile(d1, [224*224*3]), [50,224,224,3])
                d2 = np.reshape(np.tile(d2, [224*224*3]), [50,224,224,3])
                output_idx_0 = np.floor(output_idx).astype('int32')
                output_idx_1 = np.ceil(output_idx).astype('int32')
                output_idx   = output_idx.astype('int32')
            #s    import pdb; pdb.set_trace()
                output_0 = input_data[output_idx_0-1, :, :, :]
                output_1 = input_data[output_idx_1-1, :, :, :]
                d3     = output_1 - output_0

                frames = (d1/d2)*d3 + output_0
            else:
                frames, input_data, labels, names = sess.run([logits, input_data_tensor, labels_tensor, names_tensor])
                input_data = input_data[0]
            #loaded_data, labels, names = sess.run([input_data_tensor, labels_tensor, names_tensor])
            print frames


            # if vid_num==6:
            #     return frames, input_data



            # import pdb; pdb.set_trace()
        #    print names, frames

            # if model_label == 'RIL':
            #     if rate_label == 'Rate':
            #         save_gif(input_data, model_label+'_'+rate_label+'_input'+names[0][-2:-1], model, dataset, names[0][:-4])
            #         save_gif(frames, model_label+'_'+rate_label+'_output'+names[0][-2:-1], model, dataset, names[0][:-4])
            #     else:
            #         save_gif(input_data, model_label+'_'+rate_label+'_input', model, dataset, names[0])
            #         save_gif(frames, model_label+'_'+rate_label+'_output', model, dataset, names[0])
            # else:
            #     if rate_label == 'Rate':
            #     #    import pdb;pdb.set_trace()
            #         save_gif(input_data, model_label+'_'+rate_label+'_input'+names[0][-2:-1], model, dataset, names[0][:-4])
            #     #    save_gif(frames, model_label+'_'+rate_label+'_output'+str(vid_num%(vid_num_orig*10)), model, dataset, vid_num_orig)
            #     else:
            #         save_gif(input_data, model_label+'_'+rate_label+'_input', model, dataset, names[0])
            #         save_gif(frames, model_label+'_'+rate_label+'_output', model, dataset, vid_num_orig)
            #
            #








            # label = labels[0][0]
            # print "vidNum: ", vid_num
            # print "vidName: ",names
            # print "label:  ", label
        #    import pdb; pdb.set_trace()
            # if len(output_predictions.shape)!=2:
            #     output_predictions = np.mean(output_predictions, 1)
            # guess = np.mean(output_predictions, 0).argmax()
            # print "prediction: ", guess
            #
            # total_pred.append((guess, label))
            #
            # if int(guess) == int(label):
            #     acc += 1
            #
            # # END IF
            #
            # curr_logger.add_scalar_value('test/acc',acc/float(count), step=count)

        # END FOR

    # END WITH

    coord.request_stop()
    coord.join(threads)
    #
    # print "Total accuracy : ", acc/float(count)
    # print total_pred

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--model', action= 'store', required=True,
            help= 'Model architecture (c3d, lrcn, tsn, vgg16, resnet)')

    parser.add_argument('--dataset', action= 'store', required=True,
            help= 'Dataset (UCF101, HMDB51)')

    parser.add_argument('--numGpus', action= 'store', type=int, default=1,
            help = 'Number of Gpus used for calculation')

    parser.add_argument('--train', action= 'store', required=True, type=int,
            help = 'Binary value to indicate training or evaluation instance')

    parser.add_argument('--load', action='store', type=int, default=0,
            help = 'Whether you want to load a saved model to train from scratch.')

    parser.add_argument('--size', action='store', required=True, type=int,
            help = 'Input frame size')

    parser.add_argument('--inputDims', action='store', required=True, type=int,
            help = 'Input Dimensions (Number of frames to pass as input to the model)')

    parser.add_argument('--outputDims', action='store', required=True, type=int,
            help = 'Output Dimensions (Number of classes in dataset)')

    parser.add_argument('--seqLength', action='store', required=True, type=int,
            help = 'Length of sequences for LSTM')

    parser.add_argument('--expName', action='store', required=True,
            help = 'Unique name of experiment being run')

    parser.add_argument('--numVids', action='store', required=True, type=int,
            help = 'Number of videos to be used for training')

    parser.add_argument('--valNumVids', action='store', type=int,
            help = 'Number of videos to be used for validation')

    parser.add_argument('--lr', action='store', type=float, default=0.001,
            help = 'Learning Rate')

    parser.add_argument('--wd', action='store', type=float, default=0.0,
            help = 'Weight Decay')

    parser.add_argument('--nEpochs', action='store', type=int, default=1,
            help = 'Number of Epochs')

    parser.add_argument('--split', action='store', type=int, default=1,
            help = 'Dataset split to use')

    parser.add_argument('--baseDataPath', action='store', default='/z/dat',
            help = 'Path to datasets')

    parser.add_argument('--fName', action='store',
            help = 'Which dataset list to use (trainlist, testlist, vallist)')

    parser.add_argument('--saveFreq', action='store', type=int, default=1,
            help = 'Frequency in epochs to save model checkpoints')

    parser.add_argument('--valFreq', action='store', type=int, default=3,
            help = 'Frequency in epochs to validate')

    parser.add_argument('--loadedDataset', action= 'store', default='HMDB51',
            help= 'Dataset (UCF101, HMDB51)')

    parser.add_argument('--extractEnd', action= 'store', type=int, default=0,
            help= 'The parameterization network is located at the end of the model.')

    args = parser.parse_args()

    print "Setup of current experiments: ",args
    model_name = args.model


    #
    # elif model_name == 'resnet_RIL_interp_median_v23_7_2':
    #     model = ResNet_RIL_Interp_Median_v23_7_2()
    #
    # elif model_name == 'resnet_RIL_interp_median_v23_8_1':
    #     model = ResNet_RIL_Interp_Median_v23_8_1()
    #
    # elif model_name == 'resnet_RIL_interp_median_v23_8_2':
    #     model = ResNet_RIL_Interp_Median_v23_8_2()
    #
    # elif model_name == 'resnet_RIL_interp_median_v23_lstm':
    #     model = ResNet_RIL_Interp_Median_v23_lstm()
    #
    # elif model_name == 'resnet_RIL_interp_median_v24':
    #     model = ResNet_RIL_Interp_Median_v24()
    #
    # elif model_name == 'resnet_RIL_interp_median_v24_1':
    #     model = ResNet_RIL_Interp_Median_v24_1()
    #
    # elif model_name == 'resnet_RIL_interp_median_v24_lstm':
    #     model = ResNet_RIL_Interp_Median_v24_lstm()
    #
    # elif model_name == 'resnet_RIL_interp_median_v25':
    #     model = ResNet_RIL_Interp_Median_v25()
    #
    # elif model_name == 'resnet_RIL_interp_median_v26':
    #     model = ResNet_RIL_Interp_Median_v26()
    #
    # elif model_name == 'resnet_RIL_interp_median_v26_1':
    #     model = ResNet_RIL_Interp_Median_v26_1()
    #
    # elif model_name == 'resnet_RIL_interp_median_v26_2':
    #     model = ResNet_RIL_Interp_Median_v26_2()
    #
    # elif model_name == 'resnet_RIL_interp_median_v26_3':
    #     model = ResNet_RIL_Interp_Median_v26_3()
    #
    # elif model_name == 'resnet_RIL_interp_median_v27':
    #     model = ResNet_RIL_Interp_Median_v27()
    #
    # elif model_name == 'resnet_RIL_interp_median_v28':
    #     model = ResNet_RIL_Interp_Median_v28()
    #
    # elif model_name == 'resnet_RIL_interp_median_v29':
    #     model = ResNet_RIL_Interp_Median_v29()
    #
    # elif model_name == 'resnet_RIL_interp_median_v30':
    #     model = ResNet_RIL_Interp_Median_v30()
    #
    # elif model_name == 'resnet_RIL_interp_median_v31':
    #     model = ResNet_RIL_Interp_Median_v31()
    #
    # elif model_name == 'resnet_RIL_interp_median_v31_1':
    #     model = ResNet_RIL_Interp_Median_v31_1()
    #
    # elif model_name == 'resnet_RIL_interp_median_v31_2':
    #     model = ResNet_RIL_Interp_Median_v31_2()

    # elif model_name == 'resnet_RIL_interp_median_v31_3_lstm':
    #     model = ResNet_RIL_Interp_Median_v31_3_lstm()
    #
    # elif model_name == 'resnet_RIL_interp_median_v32':
    #     model = ResNet_RIL_Interp_Median_v32()
    #
    # elif model_name == 'resnet_RIL_interp_median_v33':
    #     model = ResNet_RIL_Interp_Median_v33()
    #
    # elif model_name == 'resnet_RIL_interp_median_v34':
    #     model = ResNet_RIL_Interp_Median_v34()
    #
    # elif model_name == 'resnet_RIL_interp_median_v34_1':
    #     model = ResNet_RIL_Interp_Median_v34_1()
    #
    # elif model_name == 'resnet_RIL_interp_median_v34_2':
    #     model = ResNet_RIL_Interp_Median_v34_2()
    #
    # elif model_name == 'resnet_RIL_interp_median_v34_3':
    #     model = ResNet_RIL_Interp_Median_v34_3()

    # Associating models
    if model_name == 'vgg16':
        model = VGG16(args.inputDims, 25)

    elif model_name == 'resnet':
        model = ResNet(args.inputDims, 25)

    elif model_name == 'resnet_RIL_interp_median_v23_2_1':
        model = ResNet_RIL_Interp_Median_v23_2_1(args.inputDims, 25)

    elif model_name == 'resnet_RIL_interp_median_v23_4':
        model = ResNet_RIL_Interp_Median_v23_4(args.inputDims, 25)

    elif model_name == 'resnet_RIL_interp_median_v23_7_1':
        model = ResNet_RIL_Interp_Median_v23_7_1(inputDims, 25)

    elif model_name == 'resnet_RIL_interp_median_v31_3':
        model = ResNet_RIL_Interp_Median_v31_3(args.inputDims, 25)

    elif model_name == 'resnet_RIL_interp_median_v34_3_lstm':
        model = ResNet_RIL_Interp_Median_v34_3_lstm(args.inputDims, 25)

    elif model_name == 'resnet_RIL_interp_median_v35_lstm':
        model = ResNet_RIL_Interp_Median_v35_lstm(args.inputDims, 25)

    elif model_name == 'resnet_RIL_interp_median_v36_lstm':
        model = ResNet_RIL_Interp_Median_v36_lstm(args.inputDims, 25)

    elif model_name == 'resnet_RIL_interp_median_v37_lstm':
        model = ResNet_RIL_Interp_Median_v37_lstm(args.inputDims, 25)

    elif model_name == 'resnet_RIL_interp_median_v38':
        model = ResNet_RIL_Interp_Median_v38(args.inputDims, 25)

    elif model_name == 'resnet_RIL_interp_median_v39':
        model = ResNet_RIL_Interp_Median_v39(args.inputDims, 25)

    elif model_name == 'resnet_RIL_interp_median_v40':
        model = ResNet_RIL_Interp_Median_v40(args.inputDims, 25)

    else:
        print("Model not found")

    # END IF

    if args.train:
        train(  model               = model,
                input_dims          = args.inputDims,
                output_dims         = args.outputDims,
                seq_length          = args.seqLength,
                size                = [args.size, args.size],
                num_gpus            = args.numGpus,
                dataset             = args.dataset,
                experiment_name     = args.expName,
                load_model          = args.load,
                num_vids            = args.numVids,
                val_num_vids        = args.valNumVids,
                n_epochs            = args.nEpochs,
                split               = args.split,
                base_data_path      = args.baseDataPath,
                f_name              = args.fName,
                learning_rate_init  = args.lr,
                wd                  = args.wd,
                save_freq           = args.saveFreq,
                val_freq            = args.valFreq)

    else:
        test(   model             = model,
                input_dims        = args.inputDims,
                output_dims       = args.outputDims,
                seq_length        = args.seqLength,
                size              = [args.size, args.size],
                dataset           = args.dataset,
                loaded_dataset    = args.loadedDataset,
                experiment_name   = args.expName,
                num_vids          = args.numVids,
                split             = args.split,
                base_data_path    = args.baseDataPath,
                f_name            = args.fName,
                load_model        = args.load,
                extract_end       = args.extractEnd)