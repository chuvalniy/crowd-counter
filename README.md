<div align="center">

![logo](/logo.jpg)


</div>

# People counting
Count entered / exit number of people in the store.

## Short description
In the directory there are two files for the counting enters and exits.

### Video from camera
I used YOLO along with SORT. Counting was done by crossing either the entry line or the exit line by visitors. 
A person's left bounding box must cross both boundaries for the counter to increase. The specific scenario for increasing enters/exits depends on the order in which the person crossed the lines.

### JSON file
The JSON file contains the history of the visitor’s movements with the tracking_id he already has. This algorithm differs from the previous one in that it does not count how many times the border has been crossed, but looks at the distance between the two lines relative to the visitor. If previously the visitor was close to the exit line, and in the next frame to the entry line, it means that he entered the store.

## Installation

```sh
git clone https://github.com/chuvalniy/crowd-counter
pip install -r requirements.txt
```

## How to use
For the YOLO algorithm run **src/predict/yolo.py**

For the JSON file with distance calculation run **src/predict/count.py**
