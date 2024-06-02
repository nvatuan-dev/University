from ikomia.dataprocess.workflow import Workflow
import os

try:
    #----------------------------- Step 1 -----------------------------------#
    # Create a workflow which will take your dataset as input and
    # train a YOLOv9 model on it
    #------------------------------------------------------------------------#
    wf = Workflow()

    #----------------------------- Step 2 -----------------------------------#
    # First you need to convert the COCO format to IKOMIA format.
    # Add an Ikomia dataset converter to your workflow.
    #------------------------------------------------------------------------#

    dataset = wf.add_task(name = "dataset_coco")

    dataset.set_parameters({
        "json_file": os.getcwd()+"/train/_annotations.coco.json",
        "image_folder": os.getcwd()+"/train",
        "task":"detection",
        "output_folder": os.getcwd()+"/dataset"
    })


    #----------------------------- Step 3 -----------------------------------#
    # Then, you want to train a YOLOv9 model.
    # Add YOLOv9 training algorithm to your workflow
    #------------------------------------------------------------------------#

    train = wf.add_task(name="train_yolo_v9", auto_connect=True)
    train.set_parameters({
        "model_name": "yolov9-c",
        "epochs": "20",
        "batch_size": "6",
        "train_imgsz": "640",
        "test_imgsz": "640",
        "dataset_split_ratio": "0.9",
        "output_folder": os.getcwd(),
    })


    #----------------------------- Step 4 -----------------------------------#
    # Execute your workflow.
    # It automatically runs all your tasks sequentially.
    #------------------------------------------------------------------------#
    wf.run()
except Exception as e:
    print(e)