from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UploadSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from drf_yasg import openapi
from rest_framework.status import HTTP_400_BAD_REQUEST
import os
import joblib
import cv2
import numpy as np
from keras.applications.vgg16 import VGG16
#from keras.layers import Input, Flatten, Dense, Dropout
from tensorflow.keras.layers import Input, Flatten, Dense, Dropout
from keras.models import Model as MD


class UploadFile(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description='Upload Image...',
        manual_parameters=[
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE,
                              description='Image to be uploaded'),
        ]
    )
    @action(detail=True, methods=['POST'])
    def post(self, request):
        serializer = UploadSerializer(data=request.data)


        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                HTTP_400_BAD_REQUEST
            )

        instance = serializer.save()



        print("Duong dan cua anh: ", instance.image)

        # Nhan dien
        # ...
        class_name1 = ['FreshApple','FreshBanana','FreshGrape','FreshGuava', 'FreshJujube', 'FreshOrange','FreshPomegranate','FreshStrawberry','RottenApple', 'RottenBanana', 'RottenGrape','RottenGuava','RottenJujube', 'RottenOrange', 'RottenPomegranate','RottenStrawberry']
        
        # model_ai = joblib.load('model_pbl')

        def get_model():
            model_vgg16_conv = VGG16(weights='imagenet', include_top=False)

            # Dong bang cac layer
            for layer in model_vgg16_conv.layers:
                layer.trainable = False

            # Tao model
            input = Input(shape=(128, 128, 3), name='image_input')
            output_vgg16_conv = model_vgg16_conv(input)

            # Them cac layer FC va Dropout
            x = Flatten(name='flatten')(output_vgg16_conv)
            x = Dense(4096, activation='relu', name='fc1')(x)
            x = Dropout(0.5)(x)
            x = Dense(4096, activation='relu', name='fc2')(x)
            x = Dropout(0.5)(x)
            x = Dense(16, activation='softmax', name='predictions')(x)

            # Compile
            my_model = MD(inputs=input, outputs=x)
            my_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

            return my_model

        model_ai = get_model()

        model_ai.load_weights('E:/PBL/pbl6-ai/pbl6_AI/pbl6/uploadimage/weights-45-0.91.hdf5')

        image_org = cv2.imread(str(instance.image))

        image = image_org.copy()
        image = cv2.resize(image, dsize=(128, 128))
        image = image.astype('float')*1./255
        # Convert to tensor
        image = np.expand_dims(image, axis=0)

        predict = model_ai.predict(image)
        # print('predict : ', predict)
        class_id = np.argmax(predict)

        mess = class_name1[class_id]

        print("This picture is: ", mess)
        
        # Xoa anh sau khi nhan dien
        os.remove(str(instance.image))

        return Response(str(mess))

