from ikomia.dataprocess.workflow import Workflow
from ikomia.utils.displayIO import display
import cv2
import os

# Define input video to test
video_path = 'gun.mp4' # Example: https://www.youtube.com/watch?v=EAR5jTknVOw
output_path = 'output.mp4'
# Init your workflow
wf = Workflow()

# Add object detection algorithm
detector = wf.add_task(name="infer_yolo_v9", auto_connect=True)

detector.set_parameters({
    "model_weight_file": os.getcwd()+ f'/train_result/weights/best.pt',
    "class_file": os.getcwd()+ f'/train_result/classes.yaml',
    "conf_thres": "0.2",
    "iou_thres":"0.25"
})

# Open the video file
stream = cv2.VideoCapture(video_path)
if not stream.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video properties for the output
frame_width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_rate = stream.get(cv2.CAP_PROP_FPS)

# Define the codec and create VideoWriter object
# The 'XVID' codec is widely supported and provides good quality
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_path, fourcc, frame_rate, (frame_width, frame_height))

while True:
    # Read image from stream
    ret, frame = stream.read()

    # Test if the video has ended or there is an error
    if not ret:
        print("Info: End of video or error.")
        break

    # Run the workflow on current frame
    wf.run_on(array=frame)

    # Get results
    image_out = detector.get_output(0)
    obj_detect_out = detector.get_output(1)

    # Convert the result to BGR color space for displaying
    img_out = image_out.get_image_with_mask_and_graphics(obj_detect_out)
    img_res = cv2.cvtColor(img_out, cv2.COLOR_RGB2BGR)

    # Save the resulting frame
    out.write(img_out)

    # Display
    display(img_res, title="YOLOv9 object detection", viewer="opencv")

    # Press 'q' to quit the video processing
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release everything
stream.release()
out.release()
cv2.destroyAllWindows()