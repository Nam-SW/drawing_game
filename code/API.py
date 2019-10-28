from PIL import Image
from tensorflow.keras.models import load_model
from random import randint
import numpy as np
import matplotlib.pyplot as plt


class drawing_API:
    def __init__(self):
        self.__num_of_class = 100 # 프라이빗 처리
        self.__class_name = ['lightning', 'dumbbell', 'bread', 'wheel', 'fan', 'triangle', 'mushroom', 'coffee_cup', 'hat', 'clock', 'radio', 'donut', 'car', 'syringe', 'airplane', 'spider', 'bench', 'baseball', 'shovel', 'pencil', 'flower', 'square', 'stop_sign', 'anvil', 't-shirt', 'cup', 'diving_board', 'shorts', 'power_outlet', 'wristwatch', 'beard', 'book', 'saw', 'headphones', 'axe', 'eyeglasses', 'ice_cream', 'sock', 'snake', 'bicycle', 'alarm_clock', 'mountain', 'pillow', 'line', 'ladder', 'tent', 'ceiling_fan', 'lollipop', 'smiley_face', 'cookie', 'sun', 'broom', 'key', 'tooth', 'chair', 'cloud', 'hammer', 'moon', 'basketball', 'bird', 'microphone', 'camera', 'candle', 'bed', 'frying_pan', 'cell_phone', 'bridge', 'butterfly', 'umbrella', 'tennis_racquet', 'sword', 'helmet', 'rainbow', 'door', 'face', 'suitcase', 'hot_dog', 'tree', 'rifle', 'laptop', 'traffic_light', 'paper_clip', 'spoon', 'drums', 'light_bulb', 'envelope', 'apple', 'pants', 'moustache', 'screwdriver', 'cat', 'baseball_bat', 'knife', 'grapes', 'scissors', 'star', 'eye', 'circle', 'table', 'pizza']
        self.__class_name_ko = ['번개','아령','빵','바퀴','선풍기','삼각형','버섯','커피컵','모자','시계','라디오','도넛','자동차','주사기','비행기','거미','벤치','야구','삽','연필','꽃','사각형','정지표시','모루','티셔츠','컵','다이빙도약대','반바지','전원콘센트','손목시계','턱수염','책','톱','헤드셋','도끼','안경','아이스크림','양말','뱀','자전거','알람시계','산','베개','줄','사다리','텐트','천장선풍기','막대사탕','웃는표정','쿠키','해','빗자루','열쇠','이빨','의자','구름','망치','달','농구','새','마이크','카메라','양초','침대','프라이팬','핸드폰','다리','나비','우산','테니스라켓','칼','헬멧','무지개','문','얼굴','여행가방','핫도그','나무','소총','노트북','신호등','클립','수저','드럼','전구','봉투','사과','바지','콧수염','드라이버','고양이','야구방망이','칼','포도','가위','별','눈','원','탁자','피자']
        self.__model = load_model('./quick_draw.h5')

    def check_answer(self, image):
        '''
        이미지 값을 넣어줘서 모델에서 분류를 함. 만약 상위 5개 예측에 정답이 있다면 참을 리턴. 아니면 거짓 출력
        '''
        image = Image.open(image)
        image = image.convert('L')
        image = image.resize((28, 28),Image.ANTIALIAS)
        test = np.array(image.getdata()).reshape(28, 28, 1).astype('float32')/255
        test = 1 - test
        plt.imshow(test.squeeze())
        
        pred = self.__model.predict(np.expand_dims(test, axis=0))[0]
        ind = (-pred).argsort()[:3]
        predict_en = [self.__class_name[x] for x in ind]
        predict_ko = [self.__class_name_ko[x] for x in ind]

        print(predict_en)
        print(predict_ko)

        if self.answer in predict_en:
            return False
        else:
            return predict_en[0]

    def get_rand_class(self):
        '''
        랜덤한 클래스를 리턴
        '''
        self.answer = self.__class_name[randint(0, self.__num_of_class-1)]
        return self.answer



    @property
    def class_name(self):
        return self.__class_name

    @property
    def class_name_ko(self):
        return self.__class_name_ko
    
    @property
    def num_of_class(self):
        return self.__num_of_class

    @property
    def model(self):
        return self.__model
                
