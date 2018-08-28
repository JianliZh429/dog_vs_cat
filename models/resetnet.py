from keras import layers, Model
from keras.applications import ResNet50
from keras.regularizers import l2


def build_model(num_classes, input_size):
    base_model = ResNet50(include_top=False, weights="imagenet", input_shape=(input_size, input_size, 3), pooling=None)
    #
    # for layer in base_model.layers:
    #     layer.trainable = False
    #
    x = base_model.output
    x = layers.MaxPooling2D(input_shape=base_model.layers[-1].output_shape[1:])(x)

    x = layers.Flatten()(x)

    x = layers.Dense(1024, kernel_regularizer=l2(0.0005))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation(activation='relu')(x)
    # x = layers.Dropout(0.3)(x)

    x = layers.Dense(512, kernel_regularizer=l2(0.0005))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation(activation='relu')(x)
    # x = layers.Dropout(0.3)(x)

    x = layers.Dense(128, kernel_regularizer=l2(0.0005))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation(activation='relu')(x)
    # x = layers.Dropout(0.3)(x)
    
    prediction = layers.Dense(num_classes, activation='softmax', name='fc_prediction')(x)
    model = Model(inputs=base_model.input, outputs=prediction)

    return model