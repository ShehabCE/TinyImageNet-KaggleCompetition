import numpy as np
from keras.preprocessing import image as image_utils
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import Xception
from keras.models import Model
from keras.layers import Dense
from keras.optimizers import Adam
from keras.callbacks import TensorBoard, ModelCheckpoint
import time

now = time.strftime("%c")
nb_of_classes = 200
# Fixing Seed...
np.random.seed(seed=204)
tensorboard_callback = TensorBoard(log_dir="./logs/training_" + now, histogram_freq=0, write_graph=True, write_images=False)
checkpoint_callback = ModelCheckpoint(filepath="./best_acc_weights.hdf5", verbose=1, save_best_only=True, monitor="val_acc")

### Loading Data
X_train = None
Y_train = None
X_validate = None
Y_validate = None

train_datagen = ImageDataGenerator(
    featurewise_center=True,  # set input mean to 0 over the dataset
    samplewise_center=False,  # don't set each sample mean to 0
    featurewise_std_normalization=True,  # divide all inputs by std of the dataset
    samplewise_std_normalization=False,  # don't divide each input by its std
    zca_whitening=False,  # don't apply ZCA whitening.
    rotation_range=30,  # randomly rotate images in the range (degrees, 0 to 180).
    horizontal_flip=True,  # randomly flip horizontal images.
    vertical_flip=False,  # don't randomly flip vertical images.
    zoom_range=0.1,  # slightly zoom in.
    width_shift_range=0.1,
    height_shift_range=0.1
)

validate_datagen = ImageDataGenerator(
    featurewise_center=True,  # test images should have input mean set to 0 over the images.
    featurewise_std_normalization=True,  # test images should have all divided by std of the images.
    zca_whitening=False
)

# Model Fitting with Datagen #
train_datagen.fit(X_train)
validate_datagen.fit(X_validate)

    ###     Using Xception pre-trained Network      ###
pre_trained_model = Xception(weights='imagenet', include_top=False)
x = pre_trained_model.output
    ###     Adding Layers on top of it      ###
x = Dense(1024, activation='relu')(x)
predictions = Dense(nb_of_classes, activation='softmax')(x)

    ###     Actual Model   ###
model = Model(input=pre_trained_model.input, output=predictions)
adam = Adam(lr=0.0001)
model.compile(optimizer=adam, loss='categorical_crossentropy')



model.fit_generator(train_datagen.flow_from_directory(), nb_epoch=1000,
                    validation_data= validate_datagen.flow_from_directory(),
                    verbose=1, callbacks=[tensorboard_callback, checkpoint_callback])