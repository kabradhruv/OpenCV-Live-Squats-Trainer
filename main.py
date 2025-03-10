import cv2
import mediapipe as mp
import numpy as np

class SquatTracker:
    def __init__(self, source=0):
        """
        Initializes the Squat Tracker.
        :param source: Webcam (0) or video file path
        """
        self.cap = cv2.VideoCapture(source)
        self.pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.reps = 0
        self.stage = None  # 'down' or 'up'

    def calculate_angle(self, a, b, c):
        """Calculate the angle between three points."""
        a, b, c = np.array(a), np.array(b), np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        return 360 - angle if angle > 180 else angle

    def process_frame(self, frame):
        """Process a single frame: detect pose, count reps, and provide feedback."""
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        feedback = ""  # Store feedback for user

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # Extract key points for squats
            left_hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x,
                          landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            angle = self.calculate_angle(left_hip, left_knee, left_ankle)

            # Provide feedback on squat form
            if angle > 160:
                self.stage = "up"
                feedback = "Stand tall"
            elif angle < 90:
                if self.stage == "up":
                    self.stage = "down"
                    self.reps += 1
                    feedback = "Good rep!"
                else:
                    feedback = "Go lower!"
            else:
                feedback = "Hold the position"

            # Draw landmarks and feedback
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
            cv2.putText(image, f'Angle: {int(angle)}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(image, f'Reps: {self.reps}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(image, feedback, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        return image

    def run(self):
        """Start the squat tracking application."""
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            processed_frame = self.process_frame(frame)
            cv2.imshow('Squat Tracker', processed_frame)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    print("The program is running...")
    tracker = SquatTracker()
    # tracker = SquatTracker(file_path) (Not working properly)
    tracker.run()
    print("The program has finished.")
