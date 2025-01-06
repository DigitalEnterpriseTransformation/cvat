import base64
import io
import os
import json

import torch
import numpy as np
from modelscope import snapshot_download
from PIL import Image
from model_init import Layoutlmv3_Predictor


LABEL_MAP = {
    0: 'Title',
    1: 'Text',
    2: 'Abandon',
    3: 'ImageBody',
    4: 'ImageCaption',
    5: 'TableBody',
    6: 'TableCaption',
    7: 'TableFootnote',
    8: 'InterlineEquation_Layout',
    9: 'FormulaCaption',
    13: 'InlineEquation',
    14: 'InterlineEquation_YOLO',
    15: 'OcrText',
    101: 'ImageFootnote',
}


def init_context(context):
    context.logger.info("Init context...  0%")

    # download model
    mineru_patterns = ["models/Layout/LayoutLMv3/*"]
    model_dir = snapshot_download('opendatalab/PDF-Extract-Kit-1.0', allow_patterns=mineru_patterns)
    weight_path = os.path.join(model_dir, 'models', 'Layout', 'LayoutLMv3', 'model_final.pth')
    config_path = "layoutlmv3_base_inference.yaml"

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # Read the DL model
    model = Layoutlmv3_Predictor(weight_path, config_path, device)
    context.user_data.model = model

    context.logger.info("Init context...100%")


def handler(context, event):
    context.logger.info("Run LayoutLMv3")
    data = event.body
    buf = io.BytesIO(base64.b64decode(data["image"]))
    image = np.array(Image.open(buf))
    
    elements = context.user_data.model(image)

    results = []
    for i, el in enumerate(elements):
        bbox = [el['poly'][0], el['poly'][1], el['poly'][4], el['poly'][5]]
        context.logger.info(f"{i}, {el['category_id']}, {bbox}")
        results.append({
            "confidence": str(el['score']),
            "label": LABEL_MAP[el['category_id']],
            "points": bbox,
            "type": "rectangle",
        })

    return context.Response(body=json.dumps(results), headers={},
        content_type='application/json', status_code=200)
