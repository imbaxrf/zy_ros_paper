import sys
import os
import time
import math
import numpy as np

import itertools
import struct  # get_image_size
import imghdr  # get_image_size
import cv2

def sigmoid(x):
    return 1.0 / (np.exp(-x) + 1.)


def softmax(x):
    x = np.exp(x - np.expand_dims(np.max(x, axis=1), axis=1))
    x = x / np.expand_dims(x.sum(axis=1), axis=1)
    return x


def bbox_iou(box1, box2, x1y1x2y2=True):
    
    # print('iou box1:', box1)
    # print('iou box2:', box2)

    if x1y1x2y2:
        mx = min(box1[0], box2[0])
        Mx = max(box1[2], box2[2])
        my = min(box1[1], box2[1])
        My = max(box1[3], box2[3])
        w1 = box1[2] - box1[0]
        h1 = box1[3] - box1[1]
        w2 = box2[2] - box2[0]
        h2 = box2[3] - box2[1]
    else:
        w1 = box1[2]
        h1 = box1[3]
        w2 = box2[2]
        h2 = box2[3]

        mx = min(box1[0], box2[0])
        Mx = max(box1[0] + w1, box2[0] + w2)
        my = min(box1[1], box2[1])
        My = max(box1[1] + h1, box2[1] + h2)
    uw = Mx - mx
    uh = My - my
    cw = w1 + w2 - uw
    ch = h1 + h2 - uh
    carea = 0
    if cw <= 0 or ch <= 0:
        return 0.0

    area1 = w1 * h1
    area2 = w2 * h2
    carea = cw * ch
    uarea = area1 + area2 - carea
    return carea / uarea


def nms_cpu(boxes, confs, nms_thresh=0.5, min_mode=False):
    # print(boxes.shape)
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    areas = (x2 - x1) * (y2 - y1)
    order = confs.argsort()[::-1]

    keep = []
    while order.size > 0:
        idx_self = order[0]
        idx_other = order[1:]

        keep.append(idx_self)

        xx1 = np.maximum(x1[idx_self], x1[idx_other])
        yy1 = np.maximum(y1[idx_self], y1[idx_other])
        xx2 = np.minimum(x2[idx_self], x2[idx_other])
        yy2 = np.minimum(y2[idx_self], y2[idx_other])

        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h

        if min_mode:
            over = inter / np.minimum(areas[order[0]], areas[order[1:]])
        else:
            over = inter / (areas[order[0]] + areas[order[1:]] - inter)

        inds = np.where(over <= nms_thresh)[0]
        order = order[inds + 1]
    
    return np.array(keep)

def draw_measure_line(xyxy, img, size, label, intrinsics_matrix, color=None):
    """
    :param xyxy:左上右下
    :param img:图像
    :param size 字体大小
    :param color:
    :param label:
    :param intrinsics_matrix:内参，intrinsics_matrix = [960, 540,775.9, 776.9]  # cx,cy,fx,fy
    :return:目标的位置
    """
    h = 1.45  # 相机地面高度 1.65 m
    alpha = 0 # 角度a
    # 这个这是绘制测距线用的，没什么用。你需要按照真实位置计算出地面线在图像中的位置，否则绘制出来也仅仅是个参考
    # 这个与你测量结果无关，不理解的话注释掉即可
    limit_view_width = 10.9
    limit_depth = 6.21

    u0 = intrinsics_matrix[0]  # cx
    v0 = intrinsics_matrix[1]  # cy
    fx = intrinsics_matrix[2]
    fy = intrinsics_matrix[3]
    pi = math.pi

    filter_list = [9, 11, 10, 74] # 过滤一些我不想要的类别
    if label not in filter_list:

        y = int(xyxy[3])
        x = (xyxy[0] + xyxy[2]) // 2
        #color_ground_point = (255 - np.array(color)).tolist()
        cv2.circle(img, (x, y), 3, (255,255,255), thickness=-1)

        Q_pie = [x - u0, y - v0]
        gamma_pie = math.atan(Q_pie[1] / fy) * 180 / 3.14

        beta_pie = alpha + gamma_pie

        if beta_pie == 0:
            beta_pie = 0.01

        O1Q = round(h / math.tan(beta_pie / 180 * pi), 1)

        z_in_cam = (h / math.sin(beta_pie / 180 * pi)) * math.cos(gamma_pie * pi / 180)
        x_in_cam = z_in_cam * (x - u0) / fx
        y_in_cam = z_in_cam * (y - v0) / fy
        distance = round(math.sqrt(O1Q ** 2 + x_in_cam ** 2), 2)

        # 绘制测距线#####
        temp = limit_depth * x_in_cam / z_in_cam
        temp = temp / limit_view_width
        connect_point_x = int((1 + temp) * img.shape[1] // 2)
        cv2.line(img, (x, y), (connect_point_x, img.shape[0]), (255,255,255), thickness=1)

        if distance < 0:
            distance = "unknown"
        cv2.putText(img, str(distance) + 'm', (x + size, y + size), cv2.FONT_HERSHEY_SIMPLEX, 1.0,color=(255,255,255),thickness=1)
        return np.asarray([x_in_cam, y_in_cam, z_in_cam])

def plot_boxes_cv2(img, boxes, savename=None, class_names=None, color=None):

    img = np.copy(img)
    colors = np.array([[1, 0, 1], [0, 0, 1], [0, 1, 1], [0, 1, 0], [1, 1, 0], [1, 0, 0]], dtype=np.float32)

    def get_color(c, x, max_val):
        ratio = float(x) / max_val * 5
        i = int(math.floor(ratio))
        j = int(math.ceil(ratio))
        ratio = ratio - i
        r = (1 - ratio) * colors[i][c] + ratio * colors[j][c]
        return int(r * 255)

    width = img.shape[1]
    height = img.shape[0]
    for i in range(len(boxes)):
        box = boxes[i]
        x1 = int(box[0] * width)
        y1 = int(box[1] * height)
        x2 = int(box[2] * width)
        y2 = int(box[3] * height)

        if color:
            rgb = color
        else:
            rgb = (255, 0, 0)
        if len(box) >= 7 and class_names:
            cls_conf = box[5]
            cls_id = box[6]
            '''
            print('%s: %f' % (class_names[cls_id], cls_conf))
            '''
            classes = len(class_names)
            offset = cls_id * 123457 % classes
            red = get_color(2, offset, classes)
            green = get_color(1, offset, classes)
            blue = get_color(0, offset, classes)
            if color is None:
                rgb = (red, green, blue)
            draw_measure_line([x1,y1,x2,y2], img, 20, class_names[cls_id], [640, 360,775.9, 776.9], color=None)
            img = cv2.putText(img, class_names[cls_id]+str(cls_conf)[:4], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.0, rgb, 1)
        
        img = cv2.rectangle(img, (x1, y1), (x2, y2), rgb, 1)
    if savename:
        print("save plot results to %s" % savename)
        cv2.imwrite(savename, img)
    return img


def read_truths(lab_path):
    if not os.path.exists(lab_path):
        return np.array([])
    if os.path.getsize(lab_path):
        truths = np.loadtxt(lab_path)
        truths = truths.reshape(truths.size / 5, 5)  # to avoid single truth problem
        return truths
    else:
        return np.array([])


def load_class_names(namesfile):
    class_names = []
    with open(namesfile, 'r') as fp:
        lines = fp.readlines()
    for line in lines:
        line = line.rstrip()
        class_names.append(line)
    return class_names



def post_processing(img, conf_thresh, nms_thresh, output):

    # anchors = [12, 16, 19, 36, 40, 28, 36, 75, 76, 55, 72, 146, 142, 110, 192, 243, 459, 401]
    # num_anchors = 9
    # anchor_masks = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    # strides = [8, 16, 32]
    # anchor_step = len(anchors) // num_anchors

    # [batch, num, 1, 4]
    box_array = output[0]
    # [batch, num, num_classes]
    confs = output[1]

    t1 = time.time()

    if type(box_array).__name__ != 'ndarray':
        box_array = box_array.cpu().detach().numpy()
        confs = confs.cpu().detach().numpy()

    num_classes = confs.shape[2]

    # [batch, num, 4]
    box_array = box_array[:, :, 0]

    # [batch, num, num_classes] --> [batch, num]
    max_conf = np.max(confs, axis=2)
    max_id = np.argmax(confs, axis=2)

    t2 = time.time()

    bboxes_batch = []
    for i in range(box_array.shape[0]):
       
        argwhere = max_conf[i] > conf_thresh
        l_box_array = box_array[i, argwhere, :]
        l_max_conf = max_conf[i, argwhere]
        l_max_id = max_id[i, argwhere]

        bboxes = []
        # nms for each class
        for j in range(num_classes):

            cls_argwhere = l_max_id == j
            ll_box_array = l_box_array[cls_argwhere, :]
            ll_max_conf = l_max_conf[cls_argwhere]
            ll_max_id = l_max_id[cls_argwhere]

            keep = nms_cpu(ll_box_array, ll_max_conf, nms_thresh)
            
            if (keep.size > 0):
                ll_box_array = ll_box_array[keep, :]
                ll_max_conf = ll_max_conf[keep]
                ll_max_id = ll_max_id[keep]

                for k in range(ll_box_array.shape[0]):
                    bboxes.append([ll_box_array[k, 0], ll_box_array[k, 1], ll_box_array[k, 2], ll_box_array[k, 3], ll_max_conf[k], ll_max_conf[k], ll_max_id[k]])
        
        bboxes_batch.append(bboxes)

    t3 = time.time()
    '''
    print('-----------------------------------')
    print('       max and argmax : %f' % (t2 - t1))
    print('                  nms : %f' % (t3 - t2))
    print('Post processing total : %f' % (t3 - t1))
    print('-----------------------------------')
    '''
    return bboxes_batch
