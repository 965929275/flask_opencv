# encoding:utf8
from flask import Flask,request,jsonify
from werkzeug.utils import secure_filename
import cv2
import os
app = Flask(__name__)

UPLOAD_FOLDER = os.getcwd()
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    print(UPLOAD_FOLDER)
    print(os.listdir(os.getcwd()))

    filename = secure_filename(f.filename) # 获得安全的文件名
    if 'images' not in os.listdir(UPLOAD_FOLDER):
        os.makedirs('images')
    else:
        f.save(os.path.join(UPLOAD_FOLDER+'\images',filename))
    img = cv2.imread(UPLOAD_FOLDER+'\images\\'+filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier("haar.xml")
    irons = cascade.detectMultiScale(gray, 1.1, 5, cv2.CASCADE_SCALE_IMAGE, (50, 50), (100, 100))
    irons_num = len(irons)

    if len(irons) > 0:
        for i, faceRect in enumerate(irons):
            x, y, w, h = faceRect
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2, 8, 0)
            cv2.putText(img, "#{}".format(i + 1), (int(x), int(y) - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45,(0, 0, 255), 1)  # 左上角坐标
    w = cv2.imwrite('identify-'+filename, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 保存图片
    # f.save(os.path.join(UPLOAD_FOLDER + '\images', w))
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return jsonify(
        code = 200,
        irons_num = irons_num,
        img_url = 'abs_url'
    )


if __name__ == '__main__':
    app.run()