script to convert yolo txt to labelme json
usage example:
```
python coco2json.py --width 1280 --height 720 --txt_filepath "coco_txt/1.txt" --output_json_path "example/1.json" --image_name_in_labelme_selected_dir "1.jpg" --train_class_dict_yaml_path "train_class_dict.yaml"
```
now in labelme GUI , open dir in /example


| Argument Name | Type     | Description                                                                                  | Required |
|---------------|----------|----------------------------------------------------------------------------------------------|----------|
| `--width`                     | `int`    | Width of the image                                                                           | Yes      |
| `--height`                    | `int`    | Height of the image                                                                          | Yes      |
| `--txt_filepath`              | `str`    | yolo txt file path                                                                            | Yes      |
| `--output_json_path`          | `str`    | labelme output JSON file path                                                                | Yes      |
| `--image_name_in_labelme_selected_dir` | `str`    | Image name when you select the directory in labelme                                            | Yes      |
| `--train_class_dict_yaml_path` | `str`    | Path to the train class dictionary YAML, e.g., `{0: "person", 8: "boat"}`                    | Yes      |
