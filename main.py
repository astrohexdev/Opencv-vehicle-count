import argparse
import cv2
from detector import bg_sub

def main():
    parser = argparse.ArgumentParser(description="Vehicle Detection from Video")
    parser.add_argument("--video", required=True, help="Path to video file")
    parser.add_argument("--show", default="yes", help="Show processed frame (yes/no)")
    parser.add_argument("--sub", default="no", help="Show background subtracted frame (yes/no)")

    args = parser.parse_args()

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        print("Error: Unable to open video.")
        return

    total_count = bg_sub(args.show.lower(), args.sub.lower(), cap)
    print(f"Total vehicles counted: {total_count}")

if __name__ == "__main__":
    main()
