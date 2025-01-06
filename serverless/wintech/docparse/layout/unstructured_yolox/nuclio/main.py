import base64
import io
import json

from yolox import UnstructuredYoloXModel, MODEL_TYPES
from PIL import Image
from unstructured_inference.constants import ElementType


LABEL_MAP = {
    ElementType.CAPTION: 'Caption_UNSTCTD_YOLOX',
    ElementType.FOOTNOTE: 'Footnote_UNSTCTD_YOLOX',
    ElementType.FORMULA: 'Formula_UNSTCTD_YOLOX',
    ElementType.LIST_ITEM: 'ListItem_UNSTCTD_YOLOX',
    ElementType.PAGE_FOOTER: 'PageFooter_UNSTCTD_YOLOX',
    ElementType.PAGE_HEADER: 'PageHeader_UNSTCTD_YOLOX',
    ElementType.PICTURE: 'Figure_UNSTCTD_YOLOX',
    ElementType.SECTION_HEADER: 'SectionHeader_UNSTCTD_YOLOX',
    ElementType.TABLE: 'Table_UNSTCTD_YOLOX',
    ElementType.TEXT: 'Text_UNSTCTD_YOLOX',
    ElementType.TITLE: 'Title_UNSTCTD_YOLOX',
}


def init_context(context):
    context.logger.info("Init context...  0%")

    # Read the DL model
    model = UnstructuredYoloXModel()
    model.initialize(**MODEL_TYPES['yolox'])
    context.user_data.model = model

    context.logger.info("Init context...100%")


def handler(context, event):
    context.logger.info("Run layout analysis Unstructured YoloX model")
    data = event.body
    buf = io.BytesIO(base64.b64decode(data["image"]))
    image = Image.open(buf)

    elements = context.user_data.model.predict(image)

    results = []
    for i, el in enumerate(elements.as_list()):
        bbox = [el.bbox.x1, el.bbox.y1, el.bbox.x2, el.bbox.y2]
        context.logger.info(f"{i}, {LABEL_MAP[el.type]}, {bbox}")
        results.append({
            "confidence": str(el.prob),
            "label": LABEL_MAP[el.type],
            "points": bbox,
            "type": "rectangle",
        })

    return context.Response(body=json.dumps(results), headers={},
        content_type='application/json', status_code=200)
