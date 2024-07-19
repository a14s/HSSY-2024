import numpy as np
import cv2
import cvui_edited as cvui

class RectButton():
    def __init__(self, callback, label="Button", w=50, h=35):
        self.w = w
        self.h = h
        self.callback = callback
        self.label = label
        self.state = 0
    
    def update(self, frame, x, y):
        if cvui.button(frame, x, y, self.w, self.h, self.label):
            self.state = 1
            if self.callback is not None:
                self.callback()
            self.state = 0

class TwoStateSwitch():
    def __init__(self, text="Switch", labels=["0", "1"]):
        self.text = text
        self.labels = labels
        self.value = [0]

    def update(self, frame, x, y, width, font_scale=0.3):
        try:
            # Trackbar Text
            # Switch Trackbar
            cvui.trackbar(frame, x, y, width, self.value, 0, 1, 1, '%.1Lf', cvui.TRACKBAR_DISCRETE + cvui.TRACKBAR_HIDE_LABELS + cvui.TRACKBAR_HIDE_MIN_MAX_LABELS + cvui.TRACKBAR_HIDE_STEP_SCALE + cvui.TRACKBAR_HIDE_VALUE_LABEL, 1)
            # Label Texts
            for i, label in enumerate(self.labels):
                (text_w, text_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX, font_scale, 1)
                cvui.text(frame, int(-text_w/2 + x + width*(i*2)/2), y+5, label, font_scale)
            text_y = 20
            (text_w, text_h), baseline = cv2.getTextSize(self.text+":    ", cv2.FONT_HERSHEY_COMPLEX, font_scale*1.5, 1)
            cvui.text(frame, int(x - text_w), y+text_y+5, self.text+":    ", font_scale*1.5)

        except Exception as e:
            print(f"TwoStateSwitch: update(self.main_frame, {x}, {y}, {width}, {self.value}, {self.labels}) Exception:", e)
            return -1
        return 0

class ThreeStateSwitch():
    def __init__(self, text="Switch", labels=["0", "1", "2"]):
        self.text=text
        self.labels = labels
        self.value = [0]

    def update(self, frame, x, y, width, font_scale=0.3):
        try:
            # Switch Trackbar
            cvui.trackbar(frame, x, y, width, self.value, 0, 2, 1, '%.1Lf', cvui.TRACKBAR_DISCRETE + cvui.TRACKBAR_HIDE_LABELS + cvui.TRACKBAR_HIDE_MIN_MAX_LABELS + cvui.TRACKBAR_HIDE_STEP_SCALE + cvui.TRACKBAR_HIDE_VALUE_LABEL, 1)
            # Label Texts
            for i, label in enumerate(self.labels):
                (text_w, text_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX, font_scale, 1)
                cvui.text(frame, int(-text_w/2 + x + width*(i*1.5)/3), y+5, label, font_scale)
            text_y = 20
            (text_w, text_h), baseline = cv2.getTextSize(self.text+":    ", cv2.FONT_HERSHEY_COMPLEX, font_scale*1.5, 1)
            cvui.text(frame, int(x - text_w), y+text_y+5, self.text+":    ", font_scale*1.5)

        except Exception as e:
            print(f"ThreeStateSwitch: update(self.main_frame, {x}, {y}, {width}, {self.value}, {self.labels}) Exception:", e)
            return -1
        return 0

class RaadGS():
    def __init__(self, total_width=1400, total_height=800, background_color=(49, 52, 49), window_name="Raad Ground Station"):
        self.window_name = window_name
        self.total_width = total_width
        self.total_height = total_height
        self.background_color = background_color
        self.main_frame = np.zeros((self.total_height, self.total_width, 3), np.uint8)
        self.main_frame[:] = self.background_color
        self.main_frame_copy = self.main_frame.copy()
        
        # Buttons
        self.start_button = RectButton(None, "Start", 100, 40)
        self.arm_button = RectButton(None, "Arm", 100, 40)
        self.stop_button = RectButton(None, "Stop", 100, 40)

        self.buttons = [self.start_button, self.arm_button, self.stop_button]

        # Switches
        self.mode_switch = ThreeStateSwitch(text="Mode", labels=["Manual", "Semi-Auto", "Full-Auto"])
        self.power_switch = TwoStateSwitch(text="Power", labels=["On", "Off"])
        self.tracking_status_switch = TwoStateSwitch(text="Tracking Status", labels=["Active", "Inactive"])
        self.tracking_method_switch = TwoStateSwitch(text="Tracking Method", labels=["Angle", "Velocity"])
        self.controller_status_switch = TwoStateSwitch(text="Controller Status", labels=["Active", "Inactive"])
        self.shooting_mode_switch = TwoStateSwitch(text="Shooting Mode", labels=["Single", "Burst"])
        self.shooting_status_switch = TwoStateSwitch(text="Shooting Status", labels=["Active", "Inactive"])
        self.switches = [self.power_switch, self.tracking_status_switch, self.tracking_method_switch, self.controller_status_switch, self.shooting_mode_switch, self.shooting_status_switch]

        self.value = [0]
        self.rects = {}

        cvui.init(self.window_name)

    def title(self):
        title_text = "Raad Ground Station"
        (text_w, text_h), baseline = cv2.getTextSize(title_text, cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        title_x = int((self.total_width/2) - (text_w/2))
        title_y = int((self.total_height/50))

        title_rect = cvui.Rect(title_x-5, title_y-5, text_w+5, text_h+baseline+5)
        self.rects["title"] = title_rect

        cvui.text(self.main_frame_copy, title_x, title_y, title_text, 0.8)
    
    def live_video(self, video_frame=np.array([])):
        video_x = 50
        video_y = self.rects["title"].y + self.rects["title"].height + 10
        video_width = int((self.total_width/2)-50)
        video_height = int((self.total_height - self.rects["title"].y + self.rects["title"].height + 10)/2)
        
        video_rect = cvui.Rect(video_x-5, video_y, video_width+5, video_height)
        self.rects["live_video"] = video_rect
        
        if not np.array_equal(video_frame, np.array([])):
            resized_video_frame = cv2.resize(video_frame, (video_width, video_height))
            self.main_frame_copy[video_y:video_y+video_height, video_x:video_x+video_width] = resized_video_frame
    
    def live_video2(self, video_frame=None):
        video_x = 50
        video_y = self.rects["live_video"].y + self.rects["live_video"].height
        video_width = int((self.total_width/2)-50)
        video_height = int((self.total_height - self.rects["title"].y + self.rects["title"].height + 10)/2)
        
        video_rect = cvui.Rect(video_x-5, video_y, video_width+5, video_height)
        self.rects["live_video2"] = video_rect
    
    def draw_rects(self):
        for rect in self.rects.values():
            cv2.rectangle(self.main_frame_copy, (int(rect.x), int(rect.y)), (int(rect.x + rect.width), int(rect.y + rect.height)), (255, 255, 255), 2)
    
    def render(self, video_frame=np.array([])):
        self.main_frame_copy = self.main_frame.copy()
        self.title()
        self.live_video(video_frame)
        self.live_video2()

        # self.three_state_trackbar(self.main_frame_copy, self.rects["live_video"].x+self.rects["live_video"].width+100, 400, 200)
        # self.tss2.two_state_trackbar(self.main_frame_copy, self.rects["live_video"].x+self.rects["live_video"].width+100, 500, 100)

        for b, button in enumerate(self.buttons):
            button.update(self.main_frame_copy, self.total_width-200, 200 + 50*b)

        self.mode_switch.update(self.main_frame_copy, self.rects["live_video"].x+self.rects["live_video"].width+200, 200, 200)
        for s, switch in enumerate(self.switches):
            s+=1
            switch.update(self.main_frame_copy, self.rects["live_video"].x+self.rects["live_video"].width+200, 200+50*s, 100)

        cvui.update()

        self.draw_rects()
        cvui.imshow(self.window_name, self.main_frame_copy)
        #cv2.waitKey(1)