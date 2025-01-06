from doclayout_yolo import YOLOv10
from PIL import Image


class DocLayoutYOLOModel(object):
    def __init__(self, weight, device):
        self.model = YOLOv10(weight)
        self.device = device

    def predict(self, img_pil):
        width, height = img_pil.size
        input_res = {"poly": [0, 0, width, 0, width, height, 0, height]}
        new_image, useful_list = crop_img(input_res, img_pil, crop_paste_x=width//2, crop_paste_y=0)
        paste_x, paste_y, xmin, ymin, xmax, ymax, new_width, new_height = useful_list

        layout_res = []
        doclayout_yolo_res = self.model.predict(new_image, imgsz=1024, conf=0.25, iou=0.45, verbose=True, device=self.device)[0]
        for xyxy, conf, cla in zip(doclayout_yolo_res.boxes.xyxy.cpu(), doclayout_yolo_res.boxes.conf.cpu(),
                                   doclayout_yolo_res.boxes.cls.cpu()):
            xmin, ymin, xmax, ymax = [int(p.item()) for p in xyxy]
            new_item = {
                'category_id': int(cla.item()),
                'poly': [xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax],
                'score': round(float(conf.item()), 3),
            }
            layout_res.append(new_item)

        for res in layout_res:
            p1, p2, p3, p4, p5, p6, p7, p8 = res['poly']
            p1 = p1 - paste_x
            p2 = p2 - paste_y
            p3 = p3 - paste_x
            p4 = p4 - paste_y
            p5 = p5 - paste_x
            p6 = p6 - paste_y
            p7 = p7 - paste_x
            p8 = p8 - paste_y
            res['poly'] = [p1, p2, p3, p4, p5, p6, p7, p8]

        return layout_res
    

def crop_img(input_res, input_pil_img, crop_paste_x=0, crop_paste_y=0):
    crop_xmin, crop_ymin = int(input_res['poly'][0]), int(input_res['poly'][1])
    crop_xmax, crop_ymax = int(input_res['poly'][4]), int(input_res['poly'][5])
    # Create a white background with an additional width and height of 50
    crop_new_width = crop_xmax - crop_xmin + crop_paste_x * 2
    crop_new_height = crop_ymax - crop_ymin + crop_paste_y * 2
    return_image = Image.new('RGB', (crop_new_width, crop_new_height), 'white')

    # Crop image
    crop_box = (crop_xmin, crop_ymin, crop_xmax, crop_ymax)
    cropped_img = input_pil_img.crop(crop_box)
    return_image.paste(cropped_img, (crop_paste_x, crop_paste_y))
    return_list = [crop_paste_x, crop_paste_y, crop_xmin, crop_ymin, crop_xmax, crop_ymax, crop_new_width, crop_new_height]
    return return_image, return_list
