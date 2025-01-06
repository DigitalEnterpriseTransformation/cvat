import base64
import io
import os
import json

import torch
from modelscope import snapshot_download
from PIL import Image
from DocLayoutYOLO import DocLayoutYOLOModel


LABEL_MAP = {
    0: 'Title_MNU_DLOYOLOv10',
    1: 'Text_MNU_DLOYOLOv10',
    2: 'Abandon_MNU_DLOYOLOv10',
    3: 'Figure_MNU_DLOYOLOv10',
    4: 'FigureCaption_MNU_DLOYOLOv10',
    5: 'Table_MNU_DLOYOLOv10',
    6: 'TableCaption_MNU_DLOYOLOv10',
    7: 'TableFootnote_MNU_DLOYOLOv10',
    13: 'InlineFormula_MNU_DLOYOLOv10',
    14: 'BlockFormula_MNU_DLOYOLOv10',
}


def init_context(context):
    context.logger.info("Init context...  0%")

    # download model
    mineru_patterns = ["models/Layout/YOLO/*"]
    model_dir = snapshot_download('opendatalab/PDF-Extract-Kit-1.0', allow_patterns=mineru_patterns)
    weight_path = os.path.join(model_dir, 'models', 'Layout', 'YOLO', 'doclayout_yolo_ft.pt')

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Read the DL model
    model = DocLayoutYOLOModel(weight_path, device)
    context.user_data.model = model

    context.logger.info("Init context...100%")


def handler(context, event):
    context.logger.info("Run layout analysis MinerU doclayout_yolo model")
    data = event.body
    buf = io.BytesIO(base64.b64decode(data["image"]))
    image = Image.open(buf)
    
    elements = context.user_data.model.predict(image)

    results = []
    for i, el in enumerate(elements):
        bbox = [el['poly'][0], el['poly'][1], el['poly'][4], el['poly'][5]]
        context.logger.info(f"{i}, {LABEL_MAP[el['category_id']]}, {bbox}")
        results.append({
            "confidence": str(el['score']),
            "label": LABEL_MAP[el['category_id']],
            "points": bbox,
            "type": "rectangle",
        })

    return context.Response(body=json.dumps(results), headers={},
        content_type='application/json', status_code=200)
