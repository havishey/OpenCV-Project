from PIL import Image
import io
import pytesseract
import numpy as np
import cv2 as cv
import zipfile


newfile=zipfile.ZipFile('readonly/images.zip')
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

i=0
images=[]

for names in newfile.namelist():
    name=newfile.read(names)
    newimage=io.BytesIO(name)
    images.append(Image.open(newimage))
    i+=1

text=[]
all_faces=[]
t=0
for img in images:
    text.append(pytesseract.image_to_string(img.convert('L')))
    
    faces = face_cascade.detectMultiScale(np.asarray(img),1.30)
    if faces==():
        all_faces.append([])
    else:    
        for face in faces:
            rec=face.tolist()
            all_faces.append([])
            all_faces[t].append(img.crop((rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3])))
        t+=1

def search_text(input_text):
    index=[]
    count=0
    for te in text:
        if input_text in te:
            index.append(count)
            count+=1
        else :
            count+=1
    return index

def processing_image(index):
    
    for i in index:
        if all_faces[i]==[]:
            print('Results found in a[{}] \n But there no faces in image'.format(i))
        else:
            print('Results found in a[{}]'.format(i))
            if len(all_faces[i])>5:
                contact_sheet=Image.new(all_faces[i][0].mode,(500,200))
            else:
                contact_sheet=Image.new(all_faces[i][0].mode,(500,100))
            x=0
            y=0
            for f in all_faces[i]:
                f.thumbnail((100,100))
                contact_sheet.paste(f,(x,y))
                if x+f.width == contact_sheet.width:
                    x=0
                    y=y+f.height
                else:
                    x=x+f.width
             display(contact_sheet)




            
processing_image(search_text('Christopher'))
processing_image(search_text('Mark'))





