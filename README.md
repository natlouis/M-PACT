# [M-PACT: Michigan Platform for Activity Classification in Tensorflow](https://arxiv.org/abs/1804.05879)
## Authors: Eric Hofesmann, Madan Ravi Ganesh, Jason J. Corso
## Needs to be updated 

This python framework provides modular access to common activity recognition models for the use of baseline comparisons between the current state of the art and custom models.

This README will walk you through the process of installing dependencies, downloading and formatting datasets, testing the framework, and expanding the framework to train your own models.

ATTENTION: Please cite [**the arXiv paper**](https://arxiv.org/abs/1804.05879) introducing this platform when releasing any work done using this code. 
Link: https://arxiv.org/abs/1804.05879

## Table of Contents



* [Introduction and Setup](#introduction-and-setup)
    *  [Requirements](#requirements)
	*  [Using the Framework](#using-the-framework)
	*  [Framework File Structure](#framework-file-structure)
	*  [Configuring Datasets](#configuring-datasets)
	*  [Examples of Common Uses](#examples-of-common-uses)
* [Add Custom Components](#add-custom-components)
	* [Adding a Model](#adding-a-model)
	* [Adding a Dataset](#adding-a-dataset)
* [Results](#expected-results)
* [Version History](#version-history)


## Introduction and Setup


### Implemented Models:

|  Model Architecture  |      Dataset (Split 1)      |  M-PACT Accuracy (%)  |  Original Authors Accuracy (%) |  
|:----------:|:------:| :----:| :----:|
| I3D | HMDB51 | -- |  74.80* | 
| C3D | HMDB51 | 48.24 | 50.30* | 
| TSN | HMDB51 | 51.70 |  54.40 | 
| ResNet50 + LSTM |   HMDB51   | 43.86 |  43.90  |
| I3D | UCF101 |  --  |  95.60* | 
| C3D | UCF101 |  93.66   |  82.30* | 
| TSN | UCF101 |  85.25   |  85.50 | 
| ResNet50 + LSTM |   UCF101   |  80.20  |  84.30 | 
(*) Indicates that results are shown across all three splits


### Common Datasets:

* HMDB51
* UCF101
* Kinetics
* Moments in Time


### Requirements

#### Hardware and Software:
* Nvidia Graphics Card
* Ubuntu 16.04
* Python 2.7
* Cuda
* Cudnn
* gflags

#### Python Dependencies:
* Tensorflow 1.2.1
* Numpy
* Scikit Learn
* h5py


### Using the framework

From the root directory, the training and testing is done through train_test_TFRecords_multigpu_model.py

Ex. Train ResNet50+LSTM on HMDB51 using 4 GPUs

```
python train_test_TFRecords_multigpu_model.py  --model resnet  --dataset HMDB51  --numGpus 4  --train 1  --load 0  --size 224  --inputDims 50  --outputDims 51  --seqLength 50  --expName example_1  --numVids 3570  --lr 0.001  --nEpochs 30  --split 1  --baseDataPath /data  --fName trainlist
```


The parameters to train are:

```
python  train_test_TFRecords_multigpu_model.py \

--model             The model archetecture to be used (i3d, c3d, tsn, resnet)

--dataset           The dataset to use for training (UCF101, HMDB51)

--numGpus           Number of GPUs to train on (Not yet implemented)

--train             1 or 0 whether this is a training or testing run

--load              1 or 0 whether to use the current trained checkpoints with the same experiment_name or to train from random initialized weights

--size              Size of the input frame (224 for ResNet, I3D, TSN and 112 for C3D)

--inputDims         Input dimensions (number of frames to pass into model)
    
--outputDims        Output dimensions(number of classes in dataset)

--seqLength         Sequence length to input into lstm (50 for ResNet50 and VGG16)

--expName           Experiment name

--numVids           Number of videos to train or test on within the split (Uses the first numVids videos in testlist/trainlist.txt)

--valNumVids    	Number of videos to be used for validation
    
--lr                Initial learning rate

--wd                Weight decay value, defaults to 0.0

--nEpochs           Number of epochs to train over

--split             Dataset split to use

--baseDataPath      The path to where all datasets are stored (Ex. This directory should then contain tfrecords_HMDB51/Split1/trainlist/exampleVidName.tfrecords)

--fName			    Which dataset list to use (trainlist, testlist, vallist)

--saveFreq		    Frequency in epochs to save model checkpoints (default 1 aka every epoch)

--valFreq		    Frequency in epochs to validate (default 3)

--returnLayer	    List of strings indicating parameters within the model to be tracked during training (default ['logits'])

--clipLength        Length of clips to cut video into, -1 indicates using the entire video as one clip

--videoOffset       (none or random) indicating where to begin selecting video clips assuming clipOffset is none

--clipOffset        (none or random) indicating if clips are selected sequentially or randomly

--numClips          Number of clips to break video into, -1 indicates breaking the video into the maximum number of clips based on clipLength, clipOverlap, and clipOffset

--clipOverlap       Number of frames that overlap between clips, 0 indicates no overlap and -1 indicates clips are randomly selected and not sequential

--batchSize         Number of clips to load into the model each step.

--lossType          String defining loss type associated with chosen model. (full_loss or half_loss - only compute loss based off of first half of video)

--metricsDir        Name of sub directory within experiment to store metrics. Unique directory names allow for parallel testing.

--loadedCheckpoint  Specify the step of the saved model checkpoint that will be loaded for testing. Defaults to most recent checkpoint.

--optChoice         String indicating optimizer choice

--gpuList           List of GPU IDs to be used

--gradClipValue     Value of normalized gradient at which to clip.

--lrboundary        List of boundary epochs at which lr will be updated

--lrvalues          List of lr multiplier values, length of list must equal lrboundary

--verbose           Boolean switch to display all print statements or not
```


The parameters to test are:

```
python  train_test_TFRecords_multigpu_model.py \

--model             The model archetecture to be used (ResNet50, VGG16)

--dataset           The dataset to use (UCF101, HMDB51)

--numGpus           Number of GPUs to train on (Not yet implemented)

--train             1 or 0 whether this is a training or testing run

--load              1 or 0 whether to use the current trained checkpoints with the same experiment_name or to train from random initialized weights

--size              Size of the input frame (224 for ResNet50 and VGG16)

--inputDims         Input dimensions (number of frames to pass into model)

--outputDims        Output dimensions(number of classes in dataset)

--seqLength         Sequence length to input into lstm (50 for ResNet50 and VGG16)

--expName           Experiment name

--numVids           Number of videos to train or test on within the split (Uses the first numVids videos in testlist/trainlist.txt)

--split             Dataset split to use

--baseDataPath      The path to where all datasets are stored (Ex. This directory should then contain tfrecords_HMDB51/Split1/trainlist/exampleVidName.tfrecords)

--fName			    Which dataset list to use (trainlist, testlist, vallist)

--loadedDataset	    Dataset that the model was trained on. This is to be used when testing a model on a different dataset than it was trained on.  

--returnLayer	    String indicating which layer to apply 'metricsMethod' on (default ['logits'])

--clipLength        Length of clips to cut video into, -1 indicates using the entire video as one clip

--videoOffset       (none or random) indicating where to begin selecting video clips assuming clipOffset is none

--clipOffset        (none or random) indicating if clips are selected sequentially or randomly

--numClips          Number of clips to break video into, -1 indicates breaking the video into the maximum number of clips based on clipLength, clipOverlap, and clipOffset

--clipOverlap       Number of frames that overlap between clips, 0 indicates no overlap and -1 indicates clips are randomly selected and not sequential

--metricsMethod     Which method to use to calculate accuracy metrics. (avg_pooling, last_frame, svm, svm_train or extract_features)

--batchSize         Number of clips to load into the model each step.

--metricsDir        Name of sub directory within experiment to store metrics. Unique directory names allow for parallel testing.

--loadedCheckpoint  Specify the step of the saved model checkpoint that will be loaded for testing. Defaults to most recent checkpoint.

--gpuList           List of GPU IDs to be used

--verbose           Boolean switch to display all print statements or not
```

Ex. Test C3D on UCF101 split 1

```
python train_test_TFRecords_multigpu_model.py --model c3d --dataset UCF101 --loadedDataset UCF101 --train 0 --load 1 --inputDims 16 --outputDims 101 --seqLength 1 --size 112  --expName example_2 --numClips 1 --clipLength 16 --clipOffset random --numVids 3783 --split 1 --baseDataPath /data --fName testlist
```

### Framework File Structure
```
/tf-activity-recognition-framework
   train.py  
   test.py
   create_model.py
   load_a_video.py

   /models
        /model_name
            modelname_model.py
            default_preprocessing.py
            model_weights.npy shortcut to ../weights/model_weights.npy (Optional)
            
        /weights
            model_weights.npy

   /results  
        /model_name
            /dataset_name
                /preprocessing_method
                    /experiment_name
        	            /checkpoints
        	                checkpoint
        	                checkpoint-100.npy
        	                checkpoint-100.dat
        	            /metrics_method
        	                testing_results.npy

    /logs
        /model_name
            /dataset_name
                /preprocessing_method
                    /metrics_method
                        /experiment_name
                            tensorboard_log

    /scripts
        /shell
            download_weights.sh
    
    /utils
        generate_tfrecords_dataset.py
        convert_checkpoint.py
        checkpoint_utils.py
        layers_utils.py
        metrics_utils.py
        preprocessing_utils.py
        sys_utils.py
        logger.py
        


```


train_test_TFRecords_multigpu_model.py - Main program for training and testing models
load_dataset_tfrecords.py - Loads specified dataset using a given models preprocessing
trainlist, testlist, vallist - Lists of videos for training testing and validation splits

models - Includes the model class and video preprocessing required for that model
results - Saved model weights at specified checkpoints
logs - Tensorboard logs









### Configuring Datasets


Currently integrated datasets: HMDB51, UCF101

In order to use this framework, the datasets will need to be downloaded and formatted correctly.  Datasets are not included and must be downloaded and converted to TFRecords format. Converting dataset videos into TFRecords binary files allows for optimized tensorflow data loading and processing.  

The currently methods to import and configure the datasets correctly are to either use the follow section [Adding a Dataset](#adding-a-dataset) to convert HMDB51 and UCF101 to tfrecords manually.





### Examples of Common Uses

#### Testing using existing models

Must download the saved checkpoints for the trained models with experiment names: tfrecords_resnet_HMDB51, tfrecords_vgg16_HMDB51

Test ResNet50 on HMDB51:
```
python train_test_TFRecords_multigpu_model.py  --model resnet  --dataset HMDB51  --train 0  --load 1  --size 224  --inputDims 50  --outputDims 51  --seqLength 50  --expName tfrecords_resnet_HMDB51  --numVids 1530  --split 1  --baseDataPath /z/home/madantrg/Datasets  --fName testlist
```

Test VGG16 on HMDB51:
```
python train_test_TFRecords_multigpu_model.py  --model vgg16  --dataset HMDB51  --train 0  --load 1  --size 224  --inputDims 50  --outputDims 51  --seqLength 50  --expName tfrecords_vgg16_HMDB51  --numVids 1530  --split 1  --baseDataPath /z/home/madantrg/Datasets  --fName testlist
```



#### Training models from scratch
Train ResNet50 on HMDB51:
```
python train_test_TFRecords_multigpu_model.py  --model resnet  --dataset HMDB51  --numGpus 4  --train 1  --load 0  --size 224  --inputDims 50  --outputDims 51  --seqLength 50  --expName resnet_train  --numVids 3570  --split 1  --baseDataPath /z/home/madantrg/Datasets  --fName trainlist  --lr 0.001 --wd 0.0  --nEpochs 30
```

Train VGG16 on HMDB51:
```
python train_test_TFRecords_multigpu_model.py  --model vgg16  --dataset HMDB51  --numGpus 4  --train 1  --load 0  --size 224  --inputDims 50  --outputDims 51  --seqLength 50  --expName vgg16_train  --numVids 3570  --split 1  --baseDataPath /z/home/madantrg/Datasets  --fName trainlist  --lr 0.001 --wd 0.0  --nEpochs 30
```








## Add Custom Components

### Adding a model


##### Step 1: Create Model Directory Structure

Run the python prgoram `create_model.py`:
```
python create_model.py --modelName MyModel
```


##### Step 2: Add Model Functions

Navigate to the model file:
```
/models/mymodel/mymodel_model.py
```

Required functions to fill in:

inference(): 
```
    def inference(self, inputs, is_training, input_dims, output_dims, seq_length, batch_size, scope, dropout_rate = 0.5, return_layer=['logits'], weight_decay=0.0):
        """
        Args:
            :inputs:       Input to model of shape [BatchSize x Frames x Height x Width x Channels]
            :is_training:  Boolean variable indicating phase (TRAIN OR TEST)
            :input_dims:   Length of input sequence
            :output_dims:  Integer indicating total number of classes in final prediction
            :seq_length:   Length of output sequence from LSTM
            :scope:        Scope name for current model instance
            :dropout_rate: Value indicating proability of keep inputs
            :return_layer: String matching name of a layer in current model
            :weight_decay: Double value of weight decay
            :batch_size:   Number of videos or clips to process at a time

        Return:
            :layers[return_layer]: The requested layer's output tensor
        """

        ############################################################################
        #                       Add MODELNAME Network Layers HERE                  #
        ############################################################################

        if self.verbose:
            print('Generating MODELNAME network layers')

        # END IF

        with tf.name_scope(scope, 'MODELNAME', [inputs]):
            layers = {}

            ########################################################################################
            #        TODO: Add any desired layers from layers_utils to this layers dictionary      #
            #                                                                                      #
            #       EX: layers['conv1'] = conv3d_layer(input_tensor=inputs,                        #
            #           filter_dims=[dim1, dim2, dim3, dim4],                                      #
            #           name=NAME,                                                                 #
            #           weight_decay = wd)                                                         #
            ########################################################################################


            ########################################################################################
            #       TODO: Final Layer must be 'logits'                                             #
            #                                                                                      #
            #  EX:  layers['logits'] = [fully_connected_layer(input_tensor=layers['previous'],     #
            #                                         out_dim=output_dims, non_linear_fn=None,     #
            #                                         name='out', weight_decay=weight_decay)]      #
            ########################################################################################

            layers['logits'] = # TODO Every model must return a layer named 'logits'

            layers['logits'] = tf.reshape(layers['logits'], [batch_size, seq_length, output_dims])

        # END WITH

        return [layers[x] for x in return_layer]
```

preprocess_tfrecords():
```
    def preprocess_tfrecords(self, input_data_tensor, frames, height, width, channel, input_dims, output_dims, seq_length, size, label, istraining, video_step):
        """
        Args:
            :input_data_tensor:     Data loaded from tfrecords containing either video or clips
            :frames:                Number of frames in loaded video or clip
            :height:                Pixel height of loaded video or clip
            :width:                 Pixel width of loaded video or clip
            :channel:               Number of channels in video or clip, usually 3 (RGB)
            :input_dims:            Number of frames used in input
            :output_dims:           Integer number of classes in current dataset
            :seq_length:            Length of output sequence
            :size:                  List detailing values of height and width for final frames
            :label:                 Label for loaded data
            :is_training:           Boolean value indication phase (TRAIN OR TEST)
            :video_step:            Tensorflow variable indicating the total number of videos (not clips) that have been loaded
        """

        ####################################################
        # TODO: Add more preprcessing arguments if desired #
        ####################################################

        return preprocess(input_data_tensor, frames, height, width, channel, input_dims, output_dims, seq_length, size, label, istraining, video_step, self.input_alpha)

```

loss():
```
    """ Function to return loss calculated on given network """
    def loss(self, logits, labels, loss_type):
        """
        Args:
           :logits:     Unscaled logits returned from final layer in model
           :labels:     True labels corresponding to loaded data
           :loss_type:  Allow for multiple losses that can be selected at run time. Implemented through if statements
        """

        ####################################################################################
        #  TODO: ADD CUSTOM LOSS HERE, DEFAULT IS CROSS ENTROPY LOSS                       #
        #                                                                                  #
        #   EX: labels = tf.cast(labels, tf.int64)                                         #
        #       cross_entropy_loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, #
        #                                                            logits=logits)        #
        #        return cross_entropy_loss                                                 #
        ####################################################################################
```

(Optional) load_default_weights():
```
    def load_default_weights(self):
        """
        return: Numpy dictionary containing the names and values of the weight tensors used to initialize this model
        """
    
        ############################################################################
        # TODO: Add default model weights to models/weights/ and import them here  #
        #                          ( OPTIONAL )                                    #
        #                                                                          #
        # EX: return np.load('models/weights/model_weights.npy')                   #
        #                                                                          #
        ############################################################################
```



#### Step 3: Add Model Preprocessing Steps
Navigate to the preprocessing file:
```
/models/mymodel/default_preprocessing.py
```

Required functions to fill in:

preprocess():
```
def preprocess(input_data_tensor, frames, height, width, channel, input_dims, output_dims, seq_length, size, label, istraining, video_step, input_alpha=1.0):
    """
    Preprocessing function corresponding to the chosen model
    Args:
        :input_data_tensor: Raw input data
        :frames:            Total number of frames
        :height:            Height of frame
        :width:             Width of frame
        :channel:           Total number of color channels
        :input_dims:        Number of frames to be provided as input to model
        :output_dims:       Total number of labels
        :seq_length:        Number of frames expected as output of model
        :size:              Output size of preprocessed frames
        :label:             Label of current sample
        :istraining:        Boolean indicating training or testing phase

    Return:
        Preprocessing input data and labels tensor
    """

    # Allow for resampling of input during testing for evaluation of the model's stability over video speeds
    input_data_tensor = tf.cast(input_data_tensor, tf.float32)
    input_data_tensor = resample_input(input_data_tensor, frames, frames, input_alpha)

    # Apply preprocessing related to individual frames (cropping, flipping, resize, etc.... )
    input_data_tensor = tf.map_fn(lambda img: preprocess_image(img, size[0], size[1], is_training=istraining, resize_side_min=size[0]), input_data_tensor)


    ##########################################################################################################################
    #                                                                                                                        #
    # TODO: Add any video related preprocessing (looping, resampling, etc.... Options found in utils/preprocessing_utils.py) #
    #                                                                                                                        #
    ##########################################################################################################################


    return input_data_tensor
```

preprocess_for_train():
```
def preprocess_for_train(image, output_height, output_width, resize_side):
    """Preprocesses the given image for training.
    Args:
    image: A `Tensor` representing an image of arbitrary size.
    output_height: The height of the image after preprocessing.
    output_width: The width of the image after preprocessing.
    resize_side: The smallest side of the image for aspect-preserving resizing.
    Returns:
    A preprocessed image.
    """

    ############################################################################
    #             TODO: Add preprocessing done during training phase           #
    #         Preprocessing option found in utils/preprocessing_utils.py       #
    #                                                                          #
    #  EX:    image = aspect_preserving_resize(image, resize_side)             #
    #         image = central_crop([image], output_height, output_width)[0]    #
    #         image.set_shape([output_height, output_width, 3])                #
    #         image = tf.to_float(image)                                       #
    #         return image                                                     #
    ############################################################################
```

preprocess_for_eval():
```
def preprocess_for_eval(image, output_height, output_width, resize_side):
    """Preprocesses the given image for evaluation.
    Args:
    image: A `Tensor` representing an image of arbitrary size.
    output_height: The height of the image after preprocessing.
    output_width: The width of the image after preprocessing.
    resize_side: The smallest side of the image for aspect-preserving resizing.
    Returns:
    A preprocessed image.
    """

    ############################################################################
    #             TODO: Add preprocessing done during training phase           #
    #         Preprocessing option found in utils/preprocessing_utils.py       #
    #                                                                          #
    #  EX:    image = aspect_preserving_resize(image, resize_side)             #
    #         image = central_crop([image], output_height, output_width)[0]    #
    #         image.set_shape([output_height, output_width, 3])                #
    #         image = tf.to_float(image)                                       #
    #         return image                                                     #
    ############################################################################
```






### Adding a dataset
Adding a new dataset requires that the videos converted to tfrecords and stored in a specific format. A tfrecord is simply a method of storing a video and information about the video in a binary file that is easily imported into tensorflow graphs.

Each tfrecord contains a dictionary with the following information from the original video:

* Label - Action class the video belongs to (type int64)
* Data - RGB or optical flow values for the entire video (type bytes)
* Frames - Total number of frames in the video (type int64)
* Height - Frame height in pixels (type int64)
* Width - Frame width in pixels (type int64)
* Channels - Number of channels (3 for RGB) (type int64)
* Name - Name of the video (type bytes)


The following code snipped is an example of how to convert a single video to tfrecords given the video data in the form of a numpy array.
```
def save_tfrecords(data, label, vidname, save_dir):
    filename = os.path.join(save_dir, vidname+'.tfrecords')
    writer = tf.python_io.TFRecordWriter(filename)

    features = {}
    features['Label'] = _int64(label)
    features['Data'] = _bytes(np.array(data).tostring())
    features['Frames'] = _int64(data.shape[0])
    features['Height'] = _int64(data.shape[1])
    features['Width'] = _int64(data.shape[2])
    features['Channels'] = _int64(data.shape[3])
    features['Name'] = _bytes(str(vidname))


    example = tf.train.Example(features=tf.train.Features(feature=features))
    writer.write(example.SerializeToString())
    writer.close()

def _int64(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

```
A prerequisite to this is that the video must be passed in as a numpy or python array of floats/ints which can be done a number of ways. For example using OpenCV, matplotlib, or any other desired method.

The TFRecords for each dataset must be stored in a specific file structure, HMDB51 for example:
```
/tfrecords_HMDB51
	/Split1
		/trainlist
			vidName1.tfrecords
			vidName2.tfrecords
		/testlist
		/vallist
	/Split2
	/Split3
```


## Expected Results

### Accuracies of Models
The install of this framework can be tested by comparing the output with these expected testing results of the various models trained on the datasets.

|  Model Architecture  |      Dataset (Split 1)      |  M-PACT Accuracy (%)  |  Original Authors Accuracy (%) |  
|:----------:|:------:| :----:| :----:|
| I3D | HMDB51 | -- |  74.80* | 
| C3D | HMDB51 | 48.24 | 50.30* | 
| TSN | HMDB51 | 51.70 |  54.40 | 
| ResNet50 + LSTM |   HMDB51   | 43.86 |  43.90  |
| I3D | UCF101 |  --  |  95.60* | 
| C3D | UCF101 |  93.66   |  82.30* | 
| TSN | UCF101 |  85.25   |  85.50 | 
| ResNet50 + LSTM |   UCF101   |  80.20  |  84.30 | 
(*) Indicates that results are shown across all three splits





## Version History


### Current Version: 3.0

#### Version 3.0 (GitHub Release)
Implemented TFRecords based data loading to replace HDF5 files for increased performance.  Training has been updated to allow models to be trained on multiple GPUs concurrently.  Parallel data loading has been incorporated using TFRecords queues to allow maximized use of available GPUs.  The tensorflow saver checkpoints have been replaced with a custom version which reads and writes models weights directly to numpy arrays.  This will allow existing model weights from other sources to be more easily imported into this framework. Currently validation is not compatible with this tfrecords framework.

#### Version 2.0
Implemented TFRecords based data loading to replace HDF5 files for increased performance.  Training has been updated to allow models to be trained on multiple GPUs concurrently.  Parallel data loading has been incorporated using TFRecords queues to allow maximized use of available GPUs.  The tensorflow saver checkpoints have been replaced with a custom version which reads and writes models weights directly to numpy arrays.  This will allow existing model weights from other sources to be more easily imported into this framework. Currently validation is not compatible with this tfrecords framework.

#### Version 1.0
Initial release. Using pre generated HDF5 files, test LRCN model on UCF101 dataset and train ResNet and VGG16 models on HMDB51 dataset.  Tensorboard supported, single processor and single GPU implementation with the ability to cancel and resume training every 50 steps.  Documentation includes basic overview and example of training and testing commands.

### Future features:

* Include validation during training
* Add training and testing on optical flow

