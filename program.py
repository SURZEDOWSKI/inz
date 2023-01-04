import re
import os
import torch  # YOLOv5 implemented using pytorch
import easyocr
import cv2
import pip

os.chdir(r".\yolov5")

pip.main(["install", "-r", "requirements.txt"])

model = torch.hub.load("..", "custom", "best.pt", source="local")
classes = model.names

print(torch.cuda.is_available())
print(torch.__version__)

EASY_OCR = easyocr.Reader(["en"], gpu=True)


def recognize_card_easyocr(img, coords, reader):
    # separate coordinates from box
    xmin, ymin, xmax, ymax = coords
    ncard = img[int(ymin) : int(ymax), int(xmin) : int(xmax)]  # croped card

    ocr_result = reader.readtext(ncard, detail=0)
    text = ocr_result

    filtered_text = []

    for i in range(len(text)):
        regex = re.match("^[a-zA-Z_ ].{4,}$", str(text[i]))
        if regex is not None:
            print("FOUND: ", text[i])
            filtered_text.append(text[i])

    return filtered_text


def detect_cards(frame, model):
    frame = [frame]
    results = model(frame)
    results.show()
    print(results.xyxyn[0])
    print(results.xyxyn[0][:, -1])
    print(results.xyxyn[0][:, :-1])

    labels, coordinates = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
    # print(labels, "\n", coordinates)
    return labels, coordinates


def plot_boxes(results, frame):
    # results: labels and coordinates predicted for the given frame
    # classes: contains labels

    labels, cord = results
    n = len(labels)
    x_shape, y_shape = frame.shape[1], frame.shape[0]

    card_text = []
    # looping through the detections
    for i in range(n):
        row = cord[i]
        if (
            row[4] >= 0.50
        ):  # threshold value for detection, discards everything below this value
            x1, y1, x2, y2 = (
                int(row[0] * x_shape),
                int(row[1] * y_shape),
                int(row[2] * x_shape),
                int(row[3] * y_shape),
            )  # BBox coordniates

            coords = [x1, y1, x2, y2]

            card_text.append(
                recognize_card_easyocr(img=frame, coords=coords, reader=EASY_OCR)
            )

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # BBox
            cv2.rectangle(
                frame, (x1, y1 - 20), (x2, y1), (0, 255, 0), -1
            )  # for text label background
            cv2.putText(
                frame,
                f"{card_text}",
                (x1, y1),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
            )

    print(card_text)
    return frame


frame = cv2.imread(
    "C:/Users/Wazon/Desktop/code/python/inz/dataset/val/images/34d47d2c-Zrzut_ekranu_2022-12-12_221430.png"
)
results = detect_cards(frame, model=model)
final_product = plot_boxes(results, frame)
