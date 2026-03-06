from paddleocr import PaddleOCR

ocr = PaddleOCR(lang='en')
result = ocr.ocr('test_images/tbm.jpg')
for line in result[0]:
    print(line[1][0])
