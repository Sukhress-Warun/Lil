import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def get_live_pose():
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("\rIgnoring empty camera frame.", end="")
                yield []
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            if not results.pose_landmarks:
                print("\rcant get pose", end="")
                yield []
                continue

            points = []
            for i, data_point in enumerate(results.pose_landmarks.landmark):
                if 0 <= i <= 10 or 17 <= i <= 22 or 29 <= i <= 32:
                    continue
                x, y, z = data_point.x, data_point.y, data_point.z  # ,data_point.visibility
                points.append((x, y, z))
            points = np.array(points)
            yield points
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
            # if cv2.waitKey(5) & 0xFF == 27:
            #     break
    cap.release()
