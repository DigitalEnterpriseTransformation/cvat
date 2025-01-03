import base64
import io
import json

from yolox import UnstructuredYoloXModel, MODEL_TYPES
from PIL import Image


def init_context(context):
    context.logger.info("Init context...  0%")

    # Read the DL model
    model = UnstructuredYoloXModel()
    model.initialize(**MODEL_TYPES['yolox'])
    context.user_data.model = model

    context.logger.info("Init context...100%")


def handler(context, event):
    context.logger.info("Run YoloX Layout ONNX model")
    data = event.body
    buf = io.BytesIO(base64.b64decode(data["image"]))
    image = Image.open(buf)

    elements = context.user_data.model.predict(image)

    results = []
    for i, el in enumerate(elements.as_list()):
        context.logger.info(f"{i}, {el.type}, {el.bbox}")
        results.append({
            "confidence": str(el.prob),
            "label": el.type,
            "points": [el.bbox.x1, el.bbox.y1, el.bbox.x2, el.bbox.y2],
            "type": "rectangle",
        })

    return context.Response(body=json.dumps(results), headers={},
        content_type='application/json', status_code=200)
