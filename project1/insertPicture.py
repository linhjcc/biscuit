import io
from flask import Blueprint, render_template, request
import matplotlib.pyplot as plt
from PIL import Image

from baseopensdk import BaseClient
from baseopensdk.api.base.v1 import (
    AppTableRecord,
    ListAppTableRecordRequest,
    UpdateAppTableRecordRequest,
    UpdateAppTableRecordResponse,
)
from baseopensdk.api.drive.v1 import (
    UploadAllMediaRequest,
    UploadAllMediaRequestBody,
)

picture = Blueprint('insert_picture', __name__)


def dataToLineChar(x: str, y: str, data_x: list, data_y: list):
    """
    根据提供的两列数据绘制折线图，并保存于本地
    :param x: x轴名称
    :param y: y轴名称
    :param data_x: x轴数据
    :param data_y: y轴数据
    :return: 图片存储路径
    """

    assert len(data_x) == len(data_y)

    plt.plot(data_x, data_y, marker='o')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.savefig("./static/lineChar.png")
    plt.clf()
    
    return "./static/lineChar.png"


def upload(APP_TOKEN, TABLE_ID, client, path, record_id):
    img = Image.open(path, mode='r')
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()

    request = UploadAllMediaRequest.builder() \
        .request_body(UploadAllMediaRequestBody.builder()
                      .file_name('test2.png')
                      .parent_type("bitable_image")
                      .parent_node(APP_TOKEN)
                      .size(len(imgByteArr))
                      .file(imgByteArr)
                      .build()) \
        .build()

    response = client.drive.v1.media.upload_all(request)

    file_token = response.data.file_token

    request = UpdateAppTableRecordRequest.builder() \
        .table_id(TABLE_ID) \
        .record_id(record_id) \
        .request_body(AppTableRecord.builder()
                      .fields({
        "Attachment": [{"file_token": file_token}]  # 👆🏻前面接口返回的 file_token
    })
                      .build()) \
        .build()

    response: UpdateAppTableRecordResponse = client.base.v1.app_table_record.update(request)


def insert_picture(APP_TOKEN, PERSONAL_BASE_TOKEN, TABLE_ID, field1, field2):
    # 1. 构建client
    client: BaseClient = BaseClient.builder() \
        .app_token(APP_TOKEN) \
        .personal_base_token(PERSONAL_BASE_TOKEN) \
        .build()

    # 2. 遍历记录
    list_record_request = ListAppTableRecordRequest.builder() \
        .page_size(100) \
        .table_id(TABLE_ID) \
        .build()

    list_record_response = client.base.v1.app_table_record.list(list_record_request)
    records = getattr(list_record_response.data, "items", [])

    # 3. 保存数据
    data_x = []
    data_y = []
    for record in records:
        record_id, fields = record.record_id, record.fields
        print(fields)
        x = fields.get(field1, {})
        y = fields.get(field2, {})

        if x and y:
            data_x.append(int(x))
            data_y.append(int(y))

    print(data_x)
    print(data_y)

    # 4. 画图
    picture_path = dataToLineChar(field1, field2, data_x, data_y)

    # 5.上传
    upload(APP_TOKEN, TABLE_ID, client, picture_path, records[0].record_id)

    return 'success'


@picture.route("/insert_picture", methods=['POST', 'GET'])
def insert_picture_page():
    test = ""
    if request.method == 'POST':
        APP_TOKEN = request.form['appToken']
        PERSONAL_BASE_TOKEN = request.form['personalBaseToken']
        TABLE_ID = request.form['tableSelect']

        field1 = request.form['colSelect1']
        field2 = request.form['colSelect2']
        print(field2)

        test = insert_picture(APP_TOKEN, PERSONAL_BASE_TOKEN, TABLE_ID, field1, field2)
    print(test, "aaa")
    return render_template("insert_picture.html", data=test)
