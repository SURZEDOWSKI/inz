import re
import os
import torch  # YOLOv5 implemented using pytorch
import easyocr
import cv2
import pip

from scraper import scrape_prices_from_pages, find_player_by_name

# os.chdir(r".\yolov5")

# pip.main(["install", "-r", "requirements.txt"])

print(torch.cuda.is_available())
print(torch.__version__)

EASY_OCR = easyocr.Reader(["en"], gpu=True)


def recognize_card_easyocr(img, coords, reader):
    # separate coordinates from box
    xmin, ymin, xmax, ymax = coords
    ncard = img[int(ymin) : int(ymax), int(xmin) : int(xmax)]  # croped card

    ocr_result = reader.readtext(ncard, detail=0)
    text = ocr_result

    # filtered_text = []

    for i in range(len(text)):
        text[i] = text[i].partition(" ")[0]
        regex = re.match("^[a-zA-Z_ ].{3,}$", str(text[i]))
        if regex is not None:
            print("FOUND: ", text[i])
            # filtered_text.append(text[i])
            return text[i]

    # return filtered_text


def detect_cards(frame, model):
    frame = [frame]
    results = model(frame)
    # results.show() ### uncomment to show detection results

    labels, coordinates = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
    # print(labels, "\n", coordinates)
    return labels, coordinates


def print_text(results, frame):
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

    # print(card_text)
    return card_text


def main(dictionary_links_values, links_list, img_path=None, vid_path=None):
    model = torch.hub.load(".", "custom", "best.pt", source="local")
    classes = model.names

    if img_path is not None:
        frame = cv2.imread(img_path)
        results = detect_cards(frame, model=model)
        final_product = print_text(results, frame)
        # print(final_product)
        found_links, found_values = find_player_by_name(
            dictionary_links_values, links_list, *final_product
        )
        # print(found_links, found_values)
        # return final_product
        return found_links, found_values

    elif vid_path is not None:

        ## reading the video
        cap = cv2.VideoCapture(vid_path, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # assert cap.isOpened()
        frame_no = 1

        cv2.namedWindow("press 'q' to exit", cv2.WINDOW_NORMAL)
        final_links = []
        final_prices = []
        final_product = []
        while True:
            ret, frame = cap.read()
            if ret and frame_no % 1 == 0:
                # print(f"[INFO] Working with frame {frame_no} ")

                results = detect_cards(frame, model=model)

                final_product = print_text(results, frame)
                # print(final_product)

                found_links, found_values = find_player_by_name(
                    dictionary_links_values, links_list, *final_product
                )
                # print(found_links, found_values)
                if len(found_links) != 0:
                    for i in range(len(found_links)):
                        if found_links[i] not in final_links:
                            final_links.append(found_links[i])
                            final_prices.append(found_values[i])
                # if len(found_text) is not 0:
                #    for i in range(len(found_text)):
                #        operation_text = found_text[i]
                #        if operation_text not in final_product:
                #            final_product.append(found_text)

                # print(final_product)
                cv2.imshow("press 'q' to exit", frame)

                if cv2.waitKey(5) & 0xFF == ord("q"):
                    break
                frame_no += 1

        print(f"[INFO] Clening up. . . ")

        ## closing all windows
        cv2.destroyAllWindows()
        return final_links, final_prices


if __name__ == "__main__":

    dictionary_links_values, links_list = scrape_prices_from_pages(3, 1)
    # final_links, final_prices = main(vid_path=0)
    final_links, final_prices = main(
        dictionary_links_values,
        links_list,
        img_path="C:/Users/Wazon/Desktop/code/python/inz/dataset/val/images/a437a811-Zrzut_ekranu_2022-12-12_221502.png",
    )
    # print(final_product)
    # for item in range(len(final_product)):
    #    found_links, found_values = find_player_by_name(dictionary_links_values, links_list, final_product[item])
    #    if found_links is not None:
    #        print(found_links[0], found_values[0])
    # found_links, found_values = find_player_by_name(
    #    dictionary_links_values, links_list, *final_product
    # )
    print(final_links, final_prices)


# main(vid_path=0)
