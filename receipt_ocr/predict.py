from keras.callbacks import ModelCheckpoint
from keras.utils import to_categorical
import keras.backend as K
from keras.models import load_model
import numpy as np
import cv2
import pyarabic.araby as araby
import string
letters = araby.LETTERS+string.printable+u'٠١٢٣٤٥٦٧٨٩'
test_model = load_model('test_model.h5')
test_model.load_weights('ckpts/CRNN--15--1.870.hdf5')

test_image = cv2.imread(
    'test_images/IMG_20190707_200454.jpg', 0)
test_image = cv2.resize(test_image, (432, 32))
test_image = test_image/255.0
cv2.imshow('line', test_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
test_image = np.expand_dims(test_image, -1)
test_image = np.expand_dims(test_image, axis=0)
prediction = test_model.predict(test_image)
print("prediction >>>", prediction.shape)
# use CTC decoder
out = K.get_value(K.ctc_decode(prediction, input_length=np.ones(prediction.shape[0])*prediction.shape[1],
                               greedy=True)[0][0])
print("out >>>", out)
# see the results
i = 0
text = ''
for x in out:
    print("predicted text = ", end='')
    for p in x:
        if int(p) != -1:
            print(letters[int(p)], end='')
            text += letters[int(p)]
    print('\n')
    i += 1
# with open('test_images/ff789810-8222-46b7-bf01-6fe00e37a267_prediction.txt', 'w', encoding='utf-8') as f:
#     f.write(text)
