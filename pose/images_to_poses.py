import cv2
import mediapipe as mp
import numpy as np

def images_to_poses(images, get_images_path = False):
    poses = []
    paths = []
    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5) as pose:

        for img in images:
            image = cv2.imread(img)
            try:
                image_height, image_width, _ = image.shape
                # Convert the BGR image to RGB before processing.
                results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            except:
                print("cant read", img)
                continue
            
            if not results.pose_landmarks:
                print("cant get pose from", img)
                continue
            if get_images_path:
                paths.append(img)
            points = []
            for i, data_point in enumerate(results.pose_landmarks.landmark):
                if 0 <= i <= 10 or 17 <= i <= 22 or 29 <= i <= 32:
                    continue
                x, y, z = data_point.x, data_point.y, data_point.z  # ,data_point.visibility
                points.append((x, y, z))
            poses.append(np.array(points))
    if get_images_path:
        return np.array(poses), paths
    return np.array(poses)



mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose