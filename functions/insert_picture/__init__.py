from typing import List

import io
from flask import Blueprint, render_template, request
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

from baseopensdk import BaseClient
from baseopensdk.api.base.v1 import (
    AppTableRecord,
    ListAppTableRecordRequest,
    UpdateAppTableRecordRequest,
)
from baseopensdk.api.drive.v1 import (
    UploadAllMediaRequest,
    UploadAllMediaRequestBody,
)

picture = Blueprint("insert_picture", __name__)


def dataToLinePlot(x: str, y: str, data_x: List[float], data_y: List[float]) -> str:
    assert len(data_x) == len(data_y)
    path = "./static/line_plot.png"
    plt.plot(data_x, data_y, marker="o")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.savefig(path)
    plt.clf()
    return path


def upload(APP_TOKEN: str, TABLE_ID: str, client: BaseClient, path: str, record_id: str) -> None:
    _imgByteArr = io.BytesIO()
    img = Image.open(path, mode="r")
    img.save(_imgByteArr, format="PNG")
    imgByteArr = _imgByteArr.getvalue()

    request = (
        UploadAllMediaRequest.builder()
        .request_body(
            UploadAllMediaRequestBody.builder()
            .file_name("plot.png")
            .parent_type("bitable_image")
            .parent_node(APP_TOKEN)
            .size(len(imgByteArr))
            .file(imgByteArr)
            .build()
        )
        .build()
    )
    response = client.drive.v1.media.upload_all(request)

    file_token = response.data.file_token
    request = (
        UpdateAppTableRecordRequest.builder()
        .table_id(TABLE_ID)
        .record_id(record_id)
        .request_body(
            AppTableRecord.builder()
            .fields({"Attachment": [{"file_token": file_token}]})  # 👆🏻前面接口返回的 file_token
            .build()
        )
        .build()
    )
    _ = client.base.v1.app_table_record.update(request)


def insert_picture(
    APP_TOKEN: str,
    PERSONAL_BASE_TOKEN: str,
    TABLE_ID: str,
    field1: str,
    field2: str,
) -> str:
    # 1. 构建client
    client = BaseClient.builder().app_token(APP_TOKEN).personal_base_token(PERSONAL_BASE_TOKEN).build()

    # 2. 遍历记录
    list_record_request = ListAppTableRecordRequest.builder().page_size(100).table_id(TABLE_ID).build()
    list_record_response = client.base.v1.app_table_record.list(list_record_request)
    records = getattr(list_record_response.data, "items", [])

    # 3. 保存数据
    data_x: List[float] = []
    data_y: List[float] = []
    for record in records:
        x = record.fields.get(field1, None)
        y = record.fields.get(field2, None)
        if x and y:
            data_x.append(int(x))
            data_y.append(int(y))

    # 4. 画图
    picture_path = dataToLinePlot(field1, field2, data_x, data_y)

    # 5.上传
    upload(APP_TOKEN, TABLE_ID, client, picture_path, records[0].record_id)

    return "success"


@picture.route("/insert_picture", methods=["GET", "POST"])
def insert_picture_page() -> str:
    if request.method == "POST":
        APP_TOKEN = request.form["appToken"]
        PERSONAL_BASE_TOKEN = request.form["personalBaseToken"]
        TABLE_ID = request.form["tableSelect"]

        field1 = request.form["colSelect1"]
        field2 = request.form["colSelect2"]

        resp = insert_picture(APP_TOKEN, PERSONAL_BASE_TOKEN, TABLE_ID, field1, field2)
    else:
        resp = ""
    return render_template("insert_picture.html", data=resp)
