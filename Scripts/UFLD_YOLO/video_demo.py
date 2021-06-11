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
    # 是否保存视频，保存改为True
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

        for i in range(out_j.shape[1]):
            if np.sum(out_j[:, i] != 0) > 2:
                for k in range(out_j.shape[0]):
                    if out_j[k, i] > 0:
                        ppp = (int(out_j[k, i] * col_sample_w * frame.shape[1] / 800) - 1,int(frame.shape[0] * (tusimple_row_anchor[56 - 1 - k] / 288)) - 1)
                        #ppp = (int(out_j[k, i] * col_sample_w * frame.shape[1] / 800) - 1, int(frame.shape[0] * (culane_row_anchor[18-1-k]/288)) - 1 )
                        # 画车道线点
                        cv2.circle(frame, ppp, 5, (0, 255, 0), -1)
        fps = (fps + (1. / (time.time() - t1))) / 2
        frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('result', frame)
        if cv2.waitKey(1) == 27:
            break
        if video_write:
            vout.write(frame)

