import cv2
import easyocr
import numpy as np
import time

#-------------------------------------------------------------------
def all_words():
    #LOAD
    reader = easyocr.Reader(['en'])

    #VIDEO SETUP
    cap = cv2.VideoCapture(0)

    # Optional: reduce frame size for speed
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("Error: Cannot open webcam.")
        exit()

    print("Press 'q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Optional: downscale for faster inference
        small_frame = cv2.resize(frame, (0, 0), fx=0.8, fy=0.8)

        # Run OCR (use grayscale or color — color usually works better)
        results = reader.readtext(small_frame)

        # Draw results
        for (bbox, text, prob) in results:
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            cv2.rectangle(small_frame, top_left, bottom_right, (0, 255, 0), 2)
            label = f"{text} ({prob:.2f})"
            cv2.putText(small_frame, label, (top_left[0], top_left[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Compute and display average confidence
        confidences = [prob for (_, _, prob) in results]
        avg_conf = np.mean(confidences) if confidences else 0
        cv2.putText(small_frame, f"Avg conf: {avg_conf:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        # Show the frame
        cv2.imshow("Live Text Detection", small_frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#-------------------------------------------------------------------
def preprocess_frame(frame): #helper function
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.equalizeHist(gray) #global brightness normalization
    threshold=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,10) #adaptive local contrast
    #deblurring
    sharpening_kernel=np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
    sharpened=cv2.filter2D(threshold,-1,sharpening_kernel)
    return sharpened

#-------------------------------------------------------------------
def best_word(preprocessing):
    #LOAD
    reader = easyocr.Reader(['en'])

    #VIDEO SETUP
    cap = cv2.VideoCapture(0)

    # Optional: reduce frame size for speed
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_count=0
    results=[]

    while True:
        ret,frame=cap.read()
        if not ret:
            break
        
        frame_count+=1
        if frame_count%30==0: #runs OCR every 30 frames
            ocr_frame=frame.copy()
            if preprocessing:
                ocr_frame=preprocess_frame(ocr_frame)

            results=reader.readtext(ocr_frame)

        if results:
            h,w,_=frame.shape #using original frame for color
            cx,cy=w//2,h//2 #center of image!
            best_score=-1 #initialize best confidence

            best_word=None
            for (bbox,text,prob) in results:
                if prob<0.65: 
                    continue #skip low confidence readings!

                (x1,y1),(x2,y2),(x3,y3),(x4,y4)=bbox
                word_cx=int((x1+x3)/2)
                word_cy=int((y1+y3)/2)
                distance=np.hypot(word_cx-cx,word_cy-cy)
                ratio=(1/(1+distance/250))
                score=prob*ratio

                if score>best_score:
                    best_score=score
                    best_word=(bbox,text,prob)

            if best_word:
                bbox,text,prob=best_word
                top_left=tuple(map(int,bbox[0]))
                bottom_right=tuple(map(int,bbox[2]))

                cv2.rectangle(frame,top_left,bottom_right,(0,0,255),1)
                cv2.putText(frame,f"{text} ({(prob*100):.2f})%", (top_left[0],top_left[1]-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)
                cv2.putText(frame, f"Focused word: {text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        cv2.imshow("Camera View",frame)

        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#all_words()
best_word(preprocessing=False)