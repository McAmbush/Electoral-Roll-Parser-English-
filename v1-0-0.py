import pytesseract
import cv2
import pandas as pd
import numpy as np
import os
import argparse
import fitz
import re
from PyPDF2 import PdfFileReader

Namelist = []
FNamelist = []
Vidlist = []
Name = []
FName = []
Vid = []
vt = []
vt2 = []
vt3 = []
vt4 = []
Name_f1 = []
Name_f2 = []
Name_f3 = []
li = ['Name','Father','Mother','Husband','Age','Photo','House','Available']
ap = argparse.ArgumentParser()
ap.add_argument('-f','--file',required = True,help = 'PDF File Name')
args = vars(ap.parse_args())
print('\t\t\tMozilla Public License Version 2.0\n\n')
print('Current Directory:'+args['file'])
pdf = PdfFileReader(open(args['file'],'rb'))
file_len = pdf.getNumPages()
del pdf
mat = fitz.Matrix(2.5,2.5)
bufpath = args['file'].split(sep = '/')[:-1]
out = '/'.join(bufpath)
out = out+'/temp.png'
print(out)
file = fitz.open(args['file'])
for z in range(2,file_len+1):
    print('Processing Page ',z,'.....')
    Name = []
    FName = []
    Vid = []
    vt = []
    vt2 = []
    vt3 = []
    vt4 = []
    Name_f1 = []
    Name_f2 = []
    Name_f3 = []
    page = file.loadPage(z)
    pix = page.getPixmap(mat)
    pix.writePNG(out)
    img = cv2.imread(out)
    img = cv2.resize(img,(1241,1753))
    img = cv2.cvtColor(img,cv2.COLOR_BGR2XYZ)
    i1 = img[85:230]
    i2 = img[235:375]
    i3 = img[380:515]
    i4 = img[525:670]
    i5 = img[670:810]
    i6 = img[820:960]
    i7 = img[965:1105]
    i8 = img[1110:1255]
    i9 = img[1260:1400]
    i10 = img[1405:1550]
    images = []
    images.extend((i1,i2,i3,i4,i5,i6,i7,i8,i9,i10))
    images = np.array(images)
    im = []
    for i in images:
        im.append(i[:,50:410])
        im.append(i[:,420:800])
        im.append(i[:,800:1170])
    im2 = []
    for i in im:
        im2.append(cv2.resize(i,(850,350)))
    for j in im2:
        text = pytesseract.image_to_string(j)
        x = text.split(sep = '\n')
        while '' in x:
            x.remove('')
        if len(x)<2:
            continue
        n = 0
        f = 0
        v = 0
        for j in range(len(x)):
            if x[j].startswith("Name"):
                Name.append(x[j])
                n+=1
            elif x[j].startswith("Father's Name") or x[j].startswith("Husband's Name") or x[j].startswith("Mother's Name"):
                a = x[j]
                b = x[j+1]
                FName.append(a+' '+b)
                f+=1
            else:
                    if re.search('[A-Z]',x[j]):
                        if not any(q in x[j] for q in li):
                            if len(x[j])>8:
                                if '_' not in x[j]:
                                    if re.search('[0-9]',x[j]):
                                      vt.append(x[j])
                                      v+=1
        if n==0:
            Name.append('Name : Deleted')
        if f==0:
            FName.append("FName : Deleted")
        if v==0:
            vt.append("Deleted")    
        assert len(FName)==len(Name)==len(vt)


    for i in vt:
        str5 = []
        v = ''
        if 'DL' in i and len(i.split(sep=' '))==1:
            str5.append(i)
        elif 'DL' in i:
            str5.append(i.split(sep = ' ')[-1])
        else:
            str5.append(i[-11:])
        v = ''.join(str5)
        vt2.append(v)

    for i in vt2:
        w = []
        e = ''
        q = i.split(sep = ' ')
        if len(q)>1 and q[0].isdigit():
            w.append(q[1:])
            e = ''.join(w[0])
            vt3.append(e)
        else:
            w.append(q[:])
            e = ''.join(w[0])
            vt3.append(e)

    for i in vt3:
        if len(i)>3:
            if i[3]=='O':
                x = vt3[0][:3]
                y = vt3[0][4:]
                li = [x,y]
                z = ''.join(li)
                vt4.append(z)
            else:
                vt4.append(i)
        else:
            vt4.append(i)

    Name_f1 = []
    Name_f2 = []
    Name_f3 = []
    for i in Name:
        t = i.split(sep = 'Father')
        Name_f1.append(t[0])
    for i in Name_f1:
        t = i.split(sep = 'Mother')
        Name_f2.append(t[0])
    for i in Name_f2:
        t = i.split(sep = 'Husband')
        Name_f3.append(t[0])

    Name2 = []
    for i in Name_f3:
        Name2.append(i.split(sep = ':')[1:])
    Name3 = []
    for i in Name2:
        Name3.append(i[0][1:])
    Name4 = []
    for i in Name3:
        str2 = []
        for j in i:
            if j.isalpha() or j.isspace():
                str2.append(j)
        s = ''
        t = s.join(str2)
        Name4.append(t)

    FName_f1 = []
    FName_f2 = []
    for i in FName:
        t = i.split(sep = 'House')
        FName_f1.append(t[0])
    for i in FName_f1:
        t = i.split(sep = 'Photo')
        FName_f2.append(t[0])

    FName2 = []
    for i in FName_f2:
        FName2.append(i.split(sep = ':')[1:])
    FName3 = []
    for i in FName2:
        if len(i)==0:
            FName3.append('deleted')
        else:
            FName3.append(i[0][1:])
    FName4 = []
    for i in FName3:
        str2 = []
        for j in i:
            if j.isalpha() or j.isspace():
                str2.append(j)
        s = ''
        t = s.join(str2)
        FName4.append(t)

    for x in Name4:
        Namelist.append(x)
    for x in FName4:
        FNamelist.append(x)
    for x in vt4:
        Vidlist.append(x)

df = pd.DataFrame()
df["Name"] = Namelist
df['Relation'] = FNamelist
df['Vid'] = Vidlist
save = '/'.join(bufpath)
save = save + '/outfile.csv'
df.to_csv(save)
