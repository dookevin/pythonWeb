

from PIL import Image



region = request.POST.get("region","100,200,400,500")



if region:
    try:
        region = [int(i) for i in region.split(",")]
    except:
        region = (100,200,400,500)

#print '1111111111111 :',p

img = Image.open(file_path)
x,y = img.size[0],img.size[1]

# 原图  缩略图          2

img = Image.open(file_path)
w,h = narrow(x,y,1)
img.thumbnail((w,h),Image.ANTIALIAS)
img.save("%s%s2%s" %(p,fu.name,fu.ftype))

#print 'x y :',x,y,"%s%s2%s" %(p,fu.name,fu.ftype)

##裁切图片              1   
                                          X
cropImg = img.crop(region)
#print "region :",region
cropImg.save("%s%s1%s" %(p,fu.name,fu.ftype))

#print 'x y :',x,y
#                    
## 裁剪后 缩略图     3
img.thumbnail(narrow(x,y,2),Image.ANTIALIAS)
img.save("%s%s3%s" %(p,fu.name,fu.ftype))
#print 'x y :',x,y,"%s%s3%s" %(p,fu.name,fu.ftype)












