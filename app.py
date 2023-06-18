import cv2
import imutils
import pytesseract
import smtplib
import ssl
import numpy as np







pytesseract.pytesseract.tesseract_cmd =r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

#read image file
image = cv2.imread('car.jpg')

#resize the image
image = imutils.resize(image,width=500)

cv2.imshow("Original Image",image)
#cv2.waitKey(0)

#kernal=np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
#image_s=cv2.filter2D(image,-1,kernal)

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray Scale Image",gray)
#cv2.waitKey(0)

gray = cv2.bilateralFilter(gray,11,17,17)
cv2.imshow("Smoother Image",gray)
#cv2.waitKey(0)

#ret1,bina = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
#ret2,bina_1=cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)

#blur =cv2.GaussianBlur(bina_1,(5,5),0)
edged=cv2.Canny(gray,170,200)
cv2.imshow("Canny edged",edged)
#cv2.waitKey(0)

cnts,new = cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#cnts like a curve joining allt the continous points
#RETR_LIST - it retrives all the contours but desn't create any parent-child relationship
#CHAIN_APPROX_SIMPLE -It removes all the redundant points and compress the contour by saving memory

image1 = image.copy()
cv2.drawContours(image1,cnts,-1,(0,255,0),3)
cv2.imshow("Canny after contouring",image1)
#cv2.waitKey(0)

cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:30]
NumberPlateCount = None
image2=image.copy()
cv2.drawContours(image2,cnts,-1,(0,255,0),3)
cv2.imshow("Top 30 Contours",image2)
#cv2.waitKey(0)


count =0
name =1
for i in cnts:
    perimeter = cv2.arcLength(i,True)
    approx =cv2.approxPolyDP(i,0.02*perimeter,True)
    if(len(approx)==4):
        NUmberPLateCount =approx
        x,y,w,h = cv2.boundingRect(i)
        crp_img = image[y:y+h,x:x+w]  
        cv2.imwrite(str(name)+'.png',crp_img)
        name+=1

           
        break


'''cv2.drawContours(image,[NumberPlateCount],-1,(0,255,0),3)
cv2.imshow("Final Image",image)
cv2.waitKey(0)'''   

crop_img_loc = '1.png'
cv2.imshow("Cropped Image",cv2.imread(crop_img_loc))
#cv2.waitKey(0)



text = pytesseract.image_to_string(crop_img_loc,config='--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
print("Number is : ",text)

'''
reader = easyocr.Reader(['en'],gpu=False)
result = reader.readtext(crop_img_loc)
top_left = tuple(result[0][0][0])
bottom_right =tuple(result[0][0][2])
text = result[0][1]
font = cv2.FONT_HERSHEY_SIMPLEX
img = cv2.imread(crop_img_loc)
img = cv2.rectangle(img,text,top_left,font,-5,(255,255,255),2,cv2.LINE_AA)
cv2.imshow(img)
'''



smtp_port = 587                 # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server

email_from = "bgotham047@gmail.com"
email_to = "bgotham047@gmail.com"

pswd = "bznrodlmvvqokejz"

# content of message

message = text

# Create context
simple_email_context = ssl.create_default_context()


try:
    # Connect to the server
    print("Connecting to server...")
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls(context=simple_email_context)
    TIE_server.login(email_from, pswd)
    print("Connected to server :-)")
    
    # Send the actual email
    print()
    print(f"Sending email to - {email_to}")
    TIE_server.sendmail(email_from, email_to, message)
    print(f"Email successfully sent to - {email_to}")

# If there's an error, print it out
except Exception as e:
    print(e)

# Close the port
#finally:
    #TIE_server.quit()


cv2.waitKey(0)

cv2.destroyAllWindows()