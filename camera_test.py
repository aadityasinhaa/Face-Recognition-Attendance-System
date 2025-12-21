import cv2

for backend in [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]:
    print(f"Testing backend: {backend}")
    cap = cv2.VideoCapture(0, backend)
    if cap.isOpened():
        print("✅ Camera opened")
        ret, frame = cap.read()
        print("Frame read:", ret)
        cv2.imshow("Test", frame)
        cv2.waitKey(3000)
        cap.release()
        cv2.destroyAllWindows()
        break
    else:
        print("Failed!")

