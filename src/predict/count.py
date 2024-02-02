import json

from src.utils import utils

width = 640  # Took from test-video.mp4
height = 360  # Took from test-video.mp4

detections_path = "../../data/detections.json"

enter_line, exit_line = utils.scale_cross_lines(detections_path, width, height)

# Load data
with open(detections_path, "r", encoding='utf-8') as f:
    data = json.load(f)

frames = utils.find_data_in_dictionary(data, 'frames')

# Initialize counting variables
unique_visitors = set()
exited_ids = set()
entered_ids = set()

enter_count = 0
exit_count = 0
for frame_id in frames:
    for person in frames[frame_id]['detected']['person']:
        if len(person) < 6:  # Skip visitors without track_id.
            continue

        x1, y1, x2, y2 = person[:4]
        track_id = [v['track_id'] for k, v in person[5].items()][0]  # Get track_id

        # From the thought that the number after the colon is a unique id of the visitor.
        visitor_id = int(track_id.split(":")[1])
        unique_visitors.add(visitor_id)

        # Check if a person crossed enter & exit lines for the first time.
        if (
                enter_line[0] < x1 < enter_line[2]
                and enter_line[1] - 10 < y2 < enter_line[3] + 10
                and visitor_id not in entered_ids
        ):
            if visitor_id in exited_ids:
                enter_count += 1
            entered_ids.add(visitor_id)

        if (
                exit_line[0] < x1 < exit_line[2]
                and exit_line[1] - 10 < y2 < exit_line[3] + 10
                and visitor_id not in exited_ids
        ):
            if visitor_id in entered_ids:
                exit_count += 1
            exited_ids.add(visitor_id)

# Indices of visitors may change if they leave the frame, so the number of total unique visitors is not accurate.
print("Всего: {}".format(len(unique_visitors)))

print("Вход: {}".format(enter_count))
print("Выход: {}".format(exit_count))
