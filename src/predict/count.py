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

tracking = {}
already_tracked = set()

enter_count = 0
exit_count = 0
for frame_id in frames:
    for person in frames[frame_id]['detected']['person']:
        if len(person) < 6:  # Skip visitors without track_id.
            continue

        track_id = [v['track_id'] for k, v in person[5].items()][0]  # Get track_id.

        # From the thought that the number after the colon is a unique id of the visitor.
        visitor_id = int(track_id.split(":")[1])
        unique_visitors.add(visitor_id)

        # Calculate center points
        exit_cx, exit_cy = utils.calculate_center_points(*exit_line)
        enter_cx, enter_cy = utils.calculate_center_points(*enter_line)
        cx, cy = utils.calculate_center_points(*person[:4])

        # Calculate distance between centers of person and each line. (a^2 + b^2 = c^2) => c = sqrt(a^2 + b^2)
        exit_distance = utils.find_distance(cx, exit_cx, cy, exit_cy)
        enter_distance = utils.find_distance(cx, enter_cx, cy, enter_cy)

        close_to_exit = 1 if exit_distance < enter_distance else 0
        if track_id in tracking and track_id not in already_tracked:
            if tracking[track_id] != close_to_exit:
                enter_count += 1 if close_to_exit == 1 else 0
                exit_count += 1 if close_to_exit == 0 else 0

                already_tracked.add(track_id)

        tracking[track_id] = close_to_exit


# Indices of visitors may change if they leave the frame, so the number of total unique visitors is not accurate.
print("Всего: {}".format(len(unique_visitors)))

print("Вход: {}".format(enter_count))
print("Выход: {}".format(exit_count))
