# DHL-pipline-contextual-method-service

## Service
To run the service, run ```python dhl_client.py```. The server will listen to port 5008

to use the service, send an HTTP ```POST``` request to ```(your-server-address):5008/predict```, with the request body in ```multipart/form-data``` format containing input image with key ```file```

The output will be a JSON file in the following format:
```
{
    "object_info": {
        "address" -> Detected address
        "barcode" -> Detected barcode no
        "name": -> Detected name
        "phone": -> Detected phone no
        "postcode" -> Detected postal code
        "state": -> Detected state
    },
    "resource_info": {
        "memory": -> Memory used in MB
        "time": -> Inference time
    }
}
```

# Inside Virtual Environment

If you inside a virtualenv and installing a module that has some C in it (a Python C extension module)
but then you get an error similar to this:

building 'Levenshtein' extension

creating build

creating build/temp.linux-x86_64-2.7

gcc -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -I/usr/include/python2.7 -c Levenshtein.c -o build/temp.linux-x86_64-2.7/Levenshtein.o

Levenshtein.c:99:20: fatal error: Python.h: No such file or directory

compilation terminated.

error: command 'gcc' failed with exit status 1

Solution?

```
sudo apt-get update
sudo apt-get install python-dev (so that you can have Python.h inside /usr/include/python2.x/ -> i.e /usr/include/python2.x/Python.h
```

## Dependencies
Python 3 (tested on Python 3.5.4)

Install the dependencies in ```requirements.txt``` and ```tensorflow``` or ```tensorflow-gpu```

# Additional Notes (adapted from DHL-pipline-contextual-method/README.md)

## Download Pre-trained Model
Download ```results.zip``` from the release, unzip, and put the unzipped ```results``` folder inside the project's root folder. ```results``` folder should contain:

* ```frozen_inference_graph.pb```
* ```label_map.pbtxt```
* ```pvsh``` folder
* ```test``` folder

# Additional Notes (adapted from DHL-pipline-contextual-method/README.md)

## Procedure
```model/object_detection.py``` input: raw image from DHL, output: four coordinate for address and bar code

```preprocess/crop.py``` input: coordinate from object detection, output: cropped image for image and bar code

```preprocess/deskew.py``` input: image; output: deskewed image

```preprocess/tesseract.py``` input: image; output: text after OCR

```model/classification.py``` input: image from deskew; output: a binary value whether it is printed

```model/contextual.py``` input: text from tesseract.py; output: structured final data

```test.py``` test the result for pipline.


## how to generate those files if they do not work
```model/contextual.py``` is using [this github](https://github.com/guillaumegenthial/sequence_tagging) to produce result. they produce SOTA result on coNLL classification tasks. i downloaded the fasttext embedding for thai (if you want to test on english, i used glove embedding. to produce the test data, use ```parcel_data.xls``` and ```generate_contextual_data.ipynb``` in ```extra_file``` folder

## results
for entity_linking code run:
```CUDA_VISIBLE_DEVIECS=1 python test_entity_linking.py test_images/63.png```
predictions:
```
barcode is: TDPSHO720171
preprovince ขอนแก่น
prepostcode 40000
prename อเมืองจขชอนนคน
pre_address ส.จุฑามาศ. เลิน ห้อง 610
หอสทธิลักษณ์ 473/โหมุ27 ด.ติลฯ
```
results:
```
Barcode: TDPSH07201711223
Province: ขอนแก่น
Zipcode: 40000
Name: จุฑามาศ เมลิน ห้อง610
State: ขอนแก่น
Address: หอสุทธิลักษณ์ 473/1 ม.27 ตำบลศิลา
```


for contextual NER code run:
```CUDA_VISIBLE_DEVIECS=1 python test_contextual.py test_images/63.png```


for the newest combined code run:
```CUDA_VISIBLE_DEVIECS=1 python test_contextual.py test_images/63.png```

## running time and memory taken
for cpu only
```cpu memory: 725.6MB; running time per picture: 22.2s```
for gpu and cpu
```cpu memory: 2566MB; GPU memory: 19700MB; running time per picture: 12.9s```
