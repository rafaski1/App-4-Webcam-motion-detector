"""
Webcam motion detector will detect any movement within a frame, using opencv library.
Script will trigger a webcam and compare the difference between a static frame to moving objects within a frame.
The difference will be captured as a delta frame and black and white frame.
Contours of the threshold frame will dictate the envelope of rectangular captions.
A motion time will be recorded. Data visualisation will be done using bokeh charts.
"""
import cv2, pandas
from datetime import datetime

first_frame=None
status_list=[None,None]
times=[]
df=pandas.DataFrame(columns=["Start","End"])

video=cv2.VideoCapture(0,cv2.CAP_DSHOW)

while True:
    check, frame = video.read()
    status=0 #static frame

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0) #blur removes noise and increases calculation accuracy

    if first_frame is None:
        first_frame=gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame,None,iterations=2)

    #finding contours of distinct objects on the current frame
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000: #checks if contour area is less than 1000px
            continue
        status=1 #frame with movement

        (x,y,w,h)=cv2.boundingRect(contour) #creates a rectangle
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3) #draws a rectangle
    status_list.append(status)

    status_list=status_list[-2:]

    if status_list[-1]==1 and status_list[-2]==0: #for [0,1] switch when movement happens
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2]==1: #for [0,1] switch when movement stops
        times.append(datetime.now())


    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("Contour Frame",frame)

    key=cv2.waitKey(1)

    if key ==ord("q"):
        if status==1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

#will append start and end times to pandas dataframe in csv
for i in range(0,len(times),2):
    # df["Start"]=times[i]
    # df["End"]=times[i+1]
    df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()