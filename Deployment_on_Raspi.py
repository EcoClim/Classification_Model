import gpiod
import time
import cv2
import requests
import os
import shutil 

SORTED_IMAGES_DIR = "/home/dcchs"

chip = gpiod.Chip('gpiochip0')
button_line = chip.get_line(23)  # GPIO 23
button_line.request(consumer='button', type=gpiod.LINE_REQ_DIR_IN)

in1_line = chip.get_line(17) # GPIO 17
in2_line = chip.get_line(22) # GPIO 22

in1_line.request(consumer='in1', type=gpiod.LINE_REQ_DIR_OUT)
in2_line.request(consumer='in2', type=gpiod.LINE_REQ_DIR_OUT)

SORT_DURATION = 0.7
RETURN_DURATION = 0.7

def stop():
    in1_line.set_value(0)
    in2_line.set_value(0)
    time.sleep(0.1)

def move_left():
    in1_line.set_value(0)
    in2_line.set_value(1)
    time.sleep(SORT_DURATION)
    stop()

def move_right():
    in1_line.set_value(1)
    in2_line.set_value(0)
    time.sleep(SORT_DURATION)
    stop()

def return_to_neutral_from_left():
    in1_line.set_value(1)
    in2_line.set_value(0)
    time.sleep(RETURN_DURATION)
    stop()

def return_to_neutral_from_right():
    in1_line.set_value(0)
    in2_line.set_value(1)
    time.sleep(RETURN_DURATION)
    stop()
    
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

os.makedirs(SORTED_IMAGES_DIR, exist_ok=True)

ROBOFLOW_URL = "http://localhost:9001/ecoidentify-v2.0-reycling-class/4?api_key=Os2ZluVVWRriNOylgb1Z&name=capture.jpg"

try:
    while True:
        if button_line.get_value(): 
            ret, frame = cap.read()
            if ret:
                filename_temp = "/home/dcchs/capture_temp.jpg"
                cv2.imwrite(filename_temp, frame)
                
                files = {"file": open(filename_temp, "rb")}
                resp = requests.post(ROBOFLOW_URL, files=files)
                resp_json = resp.json()
                
                prediction_made = False
                
                if resp_json.get("predictions"):
                    top_prediction = resp_json["predictions"][0]
                    prediction_class = top_prediction["class"]
                    confidence = top_prediction["confidence"]
                    
                    is_trash = (confidence < 0.75) or (prediction_class == "trash") or (prediction_class == "plastic")                  
                    if is_trash:
                        print(f"Sorting as Trash (Left). Class: {prediction_class}, Confidence: {confidence:.2f}")
                        move_left()
                        prediction_made = "left"
                    else:
                        print(f"Sorting as Recyclable (Right). Class: {prediction_class}, Confidence: {confidence:.2f}")
                        move_right()
                        prediction_made = "right"
                    
                    if prediction_made == "left":
                        return_to_neutral_from_left()
                        save_path = os.path.join(SORTED_IMAGES_DIR, f"SORTED_LEFT_{time.strftime('%Y%m%d-%H%M%S')}.jpg")
                    elif prediction_made == "right":
                        return_to_neutral_from_right()
                        save_path = os.path.join(SORTED_IMAGES_DIR, f"SORTED_RIGHT_{time.strftime('%Y%m%d-%H%M%S')}.jpg")
                        
                    shutil.move(filename_temp, save_path)
                    print(f"Saved sorted image to: {save_path}")

                files["file"].close()
                
finally:
    cap.release()
    in1_line.release()
    in2_line.release()
    button_line.release()
