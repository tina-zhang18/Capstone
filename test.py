import cv2
import easyocr
import numpy as np

#LOAD
reader = easyocr.Reader(['en'])
path='Desktop/CAPSTONE/CameraTests/test_images/'
imagename='stm.png'
image=cv2.imread(path+imagename)
results = reader.readtext(path+imagename)

#AVERAGE CONFIDENCE
confidences = [prob for (_, _, prob) in results]
average_conf = np.mean(confidences) if confidences else 0  # handle empty results
print(f"Average confidence across all detected words: {average_conf:.2f}")

#PRINTING WORDS
for bbox, text, prob in results:
    print(f"{text} (conf: {prob:.2f})")

#DRAWING ON IMAGE
for (bbox, text, prob) in results:
    # bbox is [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    top_left = tuple(map(int, bbox[0]))
    bottom_right = tuple(map(int, bbox[2]))

    # Draw rectangle
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    label = f"{text} ({prob:.2f})"

    # Put text label above rectangle
    cv2.putText(image, label, (top_left[0], top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
cv2.imshow("Detected Text", image)
cv2.waitKey(0)
cv2.destroyAllWindows()