import numpy as np
import cv2
def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation) for im in im_list]
    return cv2.vconcat(im_list_resize)

def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, ( int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation) for im in im_list]
    return cv2.hconcat(im_list_resize)

"""for i in range(9000,10000):
        print(i)
        img = cv2.imread(Dir+"ele2/energy_f"+str(i)+".png")
        img2 = cv2.imread(Dir+"elp/ele_"+str(i+1)+".png")
        im_v = hconcat_resize_min([img2, img])
        img3 = cv2.imread(Dir+"ele2_1/noon_f"+str(i)+".png")
        im_v2 = hconcat_resize_min([im_v, img3])
        height, width, layers = im_v2.shape
        size = (width,height)
        img_array.append(im_v2)
"""

cap = cv2.VideoCapture("/home/hagia-sophia/plot/motion1.mkv")
cap2 = cv2.VideoCapture("/home/hagia-sophia/plot/0001-0400.mkv")
i = 0
img = []
for i in range(400):
	ret1, frame1 = cap.read()
	ret2, frame2 = cap2.read()
	print(i)
	frame = hconcat_resize_min([frame1, frame2])
	cv2.putText(frame ,  "Ethene Dimer Metadynamics 5000 Fs",  (20, 40),  fontFace=cv2.FONT_HERSHEY_SIMPLEX,  fontScale=1,  color=(0,0,0))
	cv2.imshow('frame',frame)
    img.append(frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

out = 
cap.release()
cv2.destroyAllWindows()