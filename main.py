import argparse
from capture import VideoCaptureThread
from infer import InferenceThread
from renderer import Renderer
from config import IP_CAMERA_URL


def main():
    p = argparse.ArgumentParser(description="Shomer Real-time Person & Face Detector")
    p.add_argument(
        "--source",
        "-s",
        choices=["webcam", "ip"],
        default="webcam",
        help="Select input source: 'webcam' for local camera, 'ip' for DroidCam/IP",
    )
    args = p.parse_args()

    # escolhe entre webcam (0) ou IP
    src = IP_CAMERA_URL if args.source == "ip" else 0

    cap_thread = VideoCaptureThread(src=src)
    inf_thread = InferenceThread()
    renderer = Renderer()

    cap_thread.start()
    inf_thread.start()
    try:
        while True:
            frame = cap_thread.read()
            if frame is None:
                continue
            inf_thread.update_frame(frame)
            if inf_thread.results:
                bodies, faces = inf_thread.results
                key = renderer.draw(frame, bodies, faces)
                if key & 0xFF == ord("q"):
                    break
    finally:
        cap_thread.stop()
        inf_thread.running = False
        renderer.close()


if __name__ == "__main__":
    main()
