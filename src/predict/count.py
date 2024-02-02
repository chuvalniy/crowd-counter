from src.utils import utils

width = 640  # Took from test-video.mp4
height = 360  # Took from test-video.mp4

enter_line, exit_line = utils.scale_cross_lines("../../data/detections.json", width, height)
