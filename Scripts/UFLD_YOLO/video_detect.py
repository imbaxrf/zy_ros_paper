# -*-coding:GBK -*-
import cv2
from model.model import parsingNet
from utils.common import merge_config
from utils.dist_utils import dist_print
import torch
import scipy.special
import numpy as np
import torchvision.transforms as transforms
from PIL import Image
from data.constant import culane_row_anchor, tusimple_row_anchor
import time
import math

def is_in_poly(p, poly):
    """
    对点进行筛选，选出符合ROI特定区域内的点
    :param p: 待判断的点坐标， [x, y]
    :param poly: 多边形顶点，[[x1,y1], [x2,y2], [x3,y3], [x4,y4], ...]
    return: is_in=False则点不在范围内，删除。 is_in==True保留
    """
    px, py = p[0],p[1]
    is_in = False
    for i, corner in enumerate(poly):
        # len(poly) = 4    next_i=(0,1,2,3,0,1,2......)
        next_i = i + 1 if i + 1 < len(poly) else 0
        x1, y1 = corner
        x2, y2 = poly[next_i]
        if (x1 == px and y1 == py) or (x2 == px and y2 == py):  # if point is on vertex
            is_in = True
            break
        if min(y1, y2) < py <= max(y1, y2):  # 判断y是否处于y1与y2之间
            x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x == px:  # if point is on edge
                is_in = True
                break
            elif x > px:  # if point is on left-side of line
                is_in = True
    return is_in

def handle_point(x, y):
    """
    根据x的大小对 x,y 进行排序。再找到最大间隔，并据此把控制点分成两部分。也就是左右两条车道线
    return: 返回的是左车道线的x,y坐标以及右车道线x,y的坐标
    """
    lx = []  # 存储左车道线x坐标
    ly = []  # 存储左车道线y坐标
    rx = []  # 存储右车道线x坐标
    ry = []  # 存储右车道线y坐标
    points = zip(x, y)

    # 坐标点从小到大排序
    sorted_points = sorted(points)
    x = [point[0] for point in sorted_points]
    y = [point[1] for point in sorted_points]
    # Max存储x坐标最大间隔距离
    Max = 0
    k = 0
    # 找出x坐标最大间隔，分出左车道和右车道
    for i in range(len(x) - 1):
        # 计算欧几里得距离
        d = np.int(math.hypot(x[i + 1] - x[i], y[i + 1] - y[i]))
        if d > Max:
            Max = d
            k = i
    for i in range(len(x)):
        # 坐车道点
        if i < k + 1:
            lx.append(x[i])
            ly.append(y[i])
        # 右车道点
        else:
            rx.append(x[i])
            ry.append(y[i])
    return lx, ly, rx, ry
def poly_fitting(img,lx, ly, rx, ry):
    """
    分别对两部分控制点进行二次多项式拟合
    """
    lx = np.array(lx)
    ly = np.array(ly)
    rx = np.array(rx)
    ry = np.array(ry)
    fl = np.polyfit(ly, lx, 2)  # 用2次多项式拟合
    fr = np.polyfit(ry, rx, 2)  # 用2次多项式拟合

    # 多项式拟合
    ploty = np.linspace(450, 720, 271)
    leftx = fl[0]*ploty**2 + fl[1]*ploty + fl[2]
    rightx = fr[0]*ploty**2 + fr[1]*ploty + fr[2]

    # 提取一下需要画曲线的点
    num = []
    for i in range(len(ploty)):
        center_left = (int(leftx[i]),int(ploty[i]))
        center_right = (int(rightx[i]), int(ploty[i]))
        num.append(center_left)
        num.append(center_right)

    # 计算车辆相对于车道线中心的偏移距离
    lane_width = np.absolute(leftx[-1] - rightx[-1])
    lane_xm_per_pix = 3.7 / lane_width
    # 车辆应该保持偏移的距离
    veh_pos = (((leftx[-1] + rightx[-1]) * lane_xm_per_pix) / 2.)
    # 当前车辆偏移的距离
    cen_pos = ((img.shape[1] * lane_xm_per_pix) / 2.)
    distance_from_center = cen_pos - veh_pos
    return distance_from_center,num

def draw_values(img,distance_from_center):
    """
    将曲率和车道偏移距离里显示在图片上
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    if distance_from_center>0:
        pos_flag = 'right'
    else:
        pos_flag= 'left'
    center_text = "Vehicle is %.3fm %s of center"%(abs(distance_from_center),pos_flag)
    cv2.putText(img,center_text,(0,80), font, 1,(255,255,255),2)
    return img

test_video = 'tmp/project_video.mp4'

if __name__ == "__main__":
    torch.backends.cudnn.benchmark = True
    args, cfg = merge_config()
    dist_print('start testing...')
    assert cfg.backbone in ['18', '34', '50', '101', '152', '50next', '101next', '50wide', '101wide']

    if cfg.dataset == 'CULane':
        cls_num_per_lane = 18
    elif cfg.dataset == 'Tusimple':
        cls_num_per_lane = 56
    else:
        raise NotImplementedError

    net = parsingNet(pretrained=False, backbone=cfg.backbone, cls_dim=(cfg.griding_num + 1, cls_num_per_lane, 4),
                     use_aux=False).cuda()  # we dont need auxiliary segmentation in testing

    state_dict = torch.load(cfg.test_model, map_location='cpu')['model']
    compatible_state_dict = {}
    for k, v in state_dict.items():
        if 'module.' in k:
            compatible_state_dict[k[7:]] = v
        else:
            compatible_state_dict[k] = v

    net.load_state_dict(compatible_state_dict, strict=False)
    net.eval()

    img_transforms = transforms.Compose([
        transforms.Resize((288, 800)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])

    cap = cv2.VideoCapture(test_video)
    fps = 0.0
    # 是否保存视频
    video_write = False
    if video_write:
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        vout = cv2.VideoWriter('lane_detect.avi', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))
    print("w = {},h = {}".format(cap.get(3), cap.get(4)))
    print("cuda:{}", torch.cuda.is_available())

    poly = [(0, cap.get(4)), (460, 325), (520,350), (cap.get(3), cap.get(4))]
    while 1:
        t1 = time.time()
        # 提取筛选后的车道线点
        lane_x = []
        lane_y = []

        rval, frame = cap.read()
        if rval == False:
            break
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_ = Image.fromarray(img)  # 实现array到image的转换
        imgs = img_transforms(img_)
        imgs = imgs.unsqueeze(0)  # 起到升维的作用
        imgs = imgs.cuda()
        with torch.no_grad():
            out = net(imgs)
        col_sample = np.linspace(0, 800 - 1, cfg.griding_num)
        col_sample_w = col_sample[1] - col_sample[0]
        out_j = out[0].data.cpu().numpy()
        out_j = out_j[:, ::-1, :]
        prob = scipy.special.softmax(out_j[:-1, :, :], axis=0)
        idx = np.arange(cfg.griding_num) + 1
        idx = idx.reshape(-1, 1, 1)
        loc = np.sum(prob * idx, axis=0)
        out_j = np.argmax(out_j, axis=0)
        loc[out_j == cfg.griding_num] = 0
        out_j = loc
        # import pdb; pdb.set_trace()
        # vis = cv2.imread(os.path.join(cfg.data_root,names[0]))
        for i in range(out_j.shape[1]):
            if np.sum(out_j[:, i] != 0) > 2:
                for k in range(out_j.shape[0]):
                    if out_j[k, i] > 0:
                        ppp = (int(out_j[k, i] * col_sample_w * frame.shape[1] / 800) - 1,int(frame.shape[0] * (tusimple_row_anchor[56 - 1 - k] / 288)) - 1)
                        #ppp = (int(out_j[k, i] * col_sample_w * frame.shape[1] / 800) - 1, int(frame.shape[0] * (culane_row_anchor[18-1-k]/288)) - 1 )
                        # 对点进行筛选
                        is_in = is_in_poly(ppp,poly)
                        if is_in==True:
                            lane_x.append(ppp[0])
                            lane_y.append(ppp[1])
                            # # 画车道线点
                            # cv2.circle(frame, ppp, 5, (0, 255, 0), -1)
        lx, ly, rx, ry = handle_point(lane_x, lane_y)
        distance_from_center,num = poly_fitting(frame,lx, ly, rx, ry)
        # 每个像素点画圆,看起来像曲线，实际不是QAQ
        for i in range(len(num)):
            cv2.circle(frame,num[i], 3, (0,255,0), -1)
        draw_values(frame,distance_from_center)
        fps = (fps + (1. / (time.time() - t1))) / 2
        frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('result', frame)
        if cv2.waitKey(1) == 27:
            break
        if video_write:
            vout.write(frame)

