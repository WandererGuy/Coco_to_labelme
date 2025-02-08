import json 
import yaml
import copy

EXAMPLE_JSON = {
  "version": "5.6.1",
  "flags": {},
  "shapes": [
  ],
  "imagePath": "",
  "imageData": None,
  "imageHeight": 0,
  "imageWidth": 0
}

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def read_yolo_coor(txt_filepath):
    yolo_coor_ls = []
    with open(txt_filepath, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            value = line.split(' ')
            class_id, x_center, y_center, width, height = value
            yolo_coor_ls.append([class_id, float(x_center), float(y_center), float(width), float(height)])
    return yolo_coor_ls

def coor2coor(yolo_coor, imageWidth, imageHeight):
    x_center, y_center, width, height = yolo_coor
    x_center = x_center * imageWidth
    y_center = y_center * imageHeight
    width = width * imageWidth
    height = height * imageHeight
    x_min = x_center - width / 2
    y_min = y_center - height / 2
    x_max = x_center + width / 2
    y_max = y_center + height / 2
    return [x_min, y_min, x_max, y_max]


class Total_example_json:
    def __init__(self):
        self.result = copy.deepcopy(EXAMPLE_JSON)
        self.result["imageData"] = None
    def add_object(self, new_object_json):
        self.result["shapes"].append(new_object_json)
    def add_json_coor(self, object_json_coor, class_name):
        xmin, ymin, xmax, ymax = object_json_coor
        new_object_json = {
                "label": class_name,
                "points": [
                    [
                    xmin,
                    ymin
                    ],
                    [
                    xmax,
                    ymax
                    ]
                ],
                "group_id": None,
                "description": "",
                "shape_type": "rectangle",
                "flags": {},
                "mask": None
                }
        self.add_object(new_object_json)
    def add_image_path(self, filename):
        self.result["imagePath"] = filename
    def add_image_width_height(self, imageWidth, imageHeight):
        self.result["imageHeight"] = imageHeight
        self.result["imageWidth"] = imageWidth

class Image:
    def __init__(self, imageHeight, imageWidth, yolo_coor):
        self.imageHeight = imageHeight
        self.imageWidth = imageWidth
        self.class_id = yolo_coor[0]
        self.yolo_coor = yolo_coor[1:]
    def process_coor(self):
        x_min, y_min, x_max, y_max = coor2coor(self.yolo_coor, self.imageWidth, self.imageHeight)
        return [x_min, y_min, x_max, y_max]

def main():
    import argparse
    # Set up argument parser
    parser = argparse.ArgumentParser(description='convert coco txt to labelme json.')
    parser.add_argument('--width', type=int, help='Width of the image', required=True)
    parser.add_argument('--height', type=int, help='Height of the image', required=True)
    parser.add_argument('--txt_filepath', type=str, help='yolo txt_filepath', required=True)  # Change to str
    parser.add_argument('--output_json_path', type=str, help='labelme output_json_path', required=True)  # Change to str
    parser.add_argument('--image_name_in_labelme_selected_dir', type=str, help='when u select dir in labelme , what is name of image in that directory', required=True)  # Change to str
    parser.add_argument('--train_class_dict_yaml_path', type=str, help='train_class_dict_yaml_path, example: {0: "person", 8: "boat"}', required=True)  # Change to str

    # Parse arguments
    args = parser.parse_args()
    width = args.width
    height = args.height
    txt_filepath = args.txt_filepath
    output_json_path = args.output_json_path
    image_name_in_labelme_selected_dir = args.image_name_in_labelme_selected_dir
    train_class_dict = read_yaml(args.train_class_dict_yaml_path)
    created = False
    yolo_coor_ls = read_yolo_coor(txt_filepath)
    for yolo_coor in yolo_coor_ls:
        image = Image(imageHeight = height,
                        imageWidth = width, 
                        yolo_coor = yolo_coor)
        object_json_coor = image.process_coor()
        class_name = train_class_dict[int(image.class_id)]
        if created == False:
            res = Total_example_json()
            res.add_image_path(filename = image_name_in_labelme_selected_dir)
            res.add_image_width_height(imageWidth = width, 
                imageHeight = height)
            created = True
        res.add_json_coor(object_json_coor, class_name)
    with open(output_json_path, 'w') as file:
        json.dump(res.result, file, indent=4)

            

if __name__ == "__main__":
    main()
        
        




