import copy
import platform
import os
from imageai.Detection.Custom import CustomObjectDetection
import PySimpleGUI as sg
from PIL import Image, ImageTk
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os.path import basename
from email.mime.application import MIMEApplication
import requests
import hashlib
import cv2
from glob import glob
from time import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class SMS:
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    def __init__(self, p, a):
        self.project = p
        self.api_key = a
        self.url = 'http://sms.notisend.ru/api/'

    def doRequest(self, rqData, url):
        rqData['project'] = self.project
        l = []
        sign = ''

        for i in rqData:
            l.append(str(rqData[i]))
        l.sort()

        for element in l:
            sign += str(element) + ';'

        sign = sign + str(self.api_key)
        sign = hashlib.sha1(sign.encode("utf-8")).hexdigest()
        sign = hashlib.md5(sign.encode("utf-8")).hexdigest()
        rqData['sign'] = sign
        r = requests.get(self.url + url, headers=self.headers, params=rqData)

        print(r.text)

        return json.loads(r.text)

    def sendSMS(self, recipients, message, sender='', run_at='', test=0):
        rqData = {
            "recipients": recipients,
            "message": message,
            "test" : test
        }
        if sender != '':
            rqData['sender'] = sender
        if run_at != '':
            rqData['run_at'] = run_at
        return self.doRequest(rqData, 'message/send')


def open_window():
    def settings_window_update():
        nonlocal phone, email
        if svalues['-phone_phone-'] != '': phone = svalues['-phone_phone-']
        if svalues['-email_email-'] != '': email = svalues['-email_email-']

    def swap_text_text():
        nonlocal text_text
        buff_settings['text_view'] = not buff_settings['text_view']
        text_text = 'Вкл' if buff_settings['text_view'] else 'Выкл'
        settings_window['-text_view-'].update(text_text)

    def swap_image_text():
        nonlocal image_text
        buff_settings['image_view'] = not buff_settings['image_view']
        image_text = 'Вкл' if buff_settings['image_view'] else 'Выкл'
        settings_window['-image_view-'].update(image_text)

    def swap_phone_text():
        nonlocal phone_text, phone
        buff_settings['phone'][0] = not buff_settings['phone'][0]
        phone_text = 'Вкл' if buff_settings['phone'][0] else 'Выкл'
        settings_window['-phone-'].update(phone_text)
        if buff_settings['phone'][0]:
            settings_window['-phone_phone-'].update(phone, readonly=False)
            buff_settings['phone'][1] = phone
        else:
            settings_window['-phone_phone-'].update('', readonly=True)
            buff_settings['phone'][1] = ''

    def swap_email_text():
        nonlocal email_text, email
        buff_settings['email'][0] = not buff_settings['email'][0]
        email_text = 'Вкл' if buff_settings['email'][0] else 'Выкл'
        settings_window['-email-'].update(email_text)
        if buff_settings['email'][0]:
            settings_window['-email_email-'].update(email, readonly=False)
            buff_settings['email'][1] = email
        else:
            settings_window['-email_email-'].update('', readonly=True)
            buff_settings['email'][1] = ''

    def save():
        def phone_error(message):
            nonlocal OK
            sg.PopupOK(message, title='Ошибка')
            OK = False

        def email_error():
            nonlocal OK
            sg.PopupOK('Неверный формат email!', title='Ошибка')
            OK = False

        global settings
        OK = True
        if buff_settings['phone'][0]:
            if len(phone) in (11, 12):
                if phone[0] == '8' or phone[0:2] == '+7':
                    buff_settings['phone'][1] = phone
                else:
                    phone_error('Номер должен начинаться с +7 или 8!')
            else:
                phone_error('Номер должен содержать 11 или 12 цифр!')
        if buff_settings['email'][0]:
            if '@' in email:
                if '.' in email.split('@')[-1]:
                    buff_settings['email'][1] = email
                else:
                    email_error()
            else:
                email_error()
        if OK:
            settings = copy.deepcopy(buff_settings)
            with open('./settings.json', 'w', encoding='UTF-8') as file:
                json.dump(settings, file, indent=3, ensure_ascii=False)
        return OK

    buff_settings = copy.deepcopy(settings)
    phone = buff_settings['phone'][1]
    email = buff_settings['email'][1]
    text_text = 'Вкл' if buff_settings['text_view'] else 'Выкл'
    image_text = 'Вкл' if buff_settings['image_view'] else 'Выкл'
    phone_text = 'Вкл' if buff_settings['phone'][0] else 'Выкл'
    email_text = 'Вкл' if buff_settings['email'][0] else 'Выкл'
    settings_layout = [
        [
            sg.Button(image_text, key='-image_view-', size=(5, 1)),
            sg.Text('Выводить результат в виде изображения')
        ],
        [
            sg.Button(text_text, key='-text_view-', size=(5, 1)),
            sg.Text('Выводить результат в виде текста')
        ],
        [
            sg.Button(phone_text, key='-phone-', size=(5, 1)),
            sg.Text('Оповещение на номер'),
            sg.InputText(buff_settings['phone'][1],
                         readonly=not buff_settings['phone'][0],
                         key='-phone_phone-',
                         size=(15, 1)
                         )
        ],
        [
            sg.Button(email_text, key='-email-', size=(5, 1)),
            sg.Text('Оповещение на почту '),
            sg.InputText(buff_settings['email'][1],
                         readonly=not buff_settings['email'][0],
                         key='-email_email-',
                         size=(15, 1)
                         )
        ],
        [
            sg.VPush()
        ],
        [
            sg.Button('Сохранить', key='-save_set-'),
            sg.Push(),
            sg.Button('Отменить', key='-cancel-')
        ]
    ]
    settings_window = sg.Window("Настройки", settings_layout, modal=True, size=(300, 170))
    while True:
        sevent, svalues = settings_window.read()
        if sevent in ("Exit", sg.WIN_CLOSED, '-cancel-'):
            break
        settings_window_update()
        if sevent == '-text_view-':
            swap_text_text()
            if not buff_settings['image_view'] and not buff_settings['text_view']:
                swap_image_text()
        if sevent == '-image_view-':
            swap_image_text()
            if not buff_settings['text_view'] and not buff_settings['image_view']:
                swap_text_text()
        if sevent == '-phone-':
            swap_phone_text()
        if sevent == '-email-':
            swap_email_text()
        if sevent == '-save_set-':
            if save():
                settings_window.close()
                return True

    settings_window.close()


def collect(video_path):
    video = cv2.VideoCapture(video_path)
    successful_detection, successful_images = [], []

    fps = int(round(video.get(cv2.CAP_PROP_FPS), 0))
    # frame_count = int(round(video.get(cv2.CAP_PROP_FRAME_COUNT), 0))
    # print(fps, frame_count)
    # print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
    count = 0
    success = True

    frames = './frames/'
    if not os.path.isdir(frames):
        os.mkdir(frames)
    files = glob(frames + '*')
    for f in files:
        os.remove(f)

    det = './detects/'
    if not os.path.isdir(det):
        os.mkdir(det)
    files = glob(det +'*')
    for f in files:
        os.remove(f)

    while success:
        success, image = video.read()
        # print('read a new frame:',success)
        if count % fps == 0:
            name = frames +'frame' + str(count).zfill(8) + '.png'
            cv2.imwrite(name, image)
            detections = detect(name, name.replace('frame', 'detect'))
            # print(detections)
            if len(detections) > 0:
                new_name = name.replace('./frames/', '').replace('frame', 'detect').split('/')[-1]
                successful_images.append(new_name)
                successful_detection.append(detections)
        count += 1

    return successful_detection, successful_images


def detect(img_path, output):
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("./epoch_79.h5")
    detector.setJsonPath("./detection_config.json")
    detector.loadModel()
    return detector.detectObjectsFromImage(input_image=img_path, output_image_path=output)


def show_img(image_path):
    try:
        image = Image.open(image_path)
        image.thumbnail((320, 320))
        photo_img = ImageTk.PhotoImage(image)
        window["-IMG-"].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")


file_types = [
    ('All png files', '*.png'),
    ('All jpg files', '*.jpg'),
    ('All jpeg files', '*.jpeg'),
    ('All mp4 files', '*.mp4'),
    ('All avi files', '*.aci')
]


def create_window(video=False):
    global text_view, image_view
    text_out_column = [
        [sg.Multiline(key='-OUT-', size=(52, 28), text_color='darkblue', disabled=True)]
    ]

    image_viewer_column = [
        [sg.Image(key='-IMG-', size=(320, 280), background_color='#86A6DF')],
        [
            sg.Push(), sg.Button('Пред', key='-prev-', visible=video),
            sg.Button('След', key='-next-', visible=video), sg.Push()
        ]
    ]

    buttons = [[sg.Button('Анализ', key='-ANALYSIS-', disabled=True, button_color='gray'), sg.Push()],
               [sg.Push() for _ in range(1) if text_view and image_view],
               [sg.Button('Очистить', key='-CLR-', visible=text_view)],
               [sg.Push() for _ in range(3) if text_view and image_view]]

    layout = [
        [sg.Input(key='-filebrowse-', enable_events=True, visible=False)],
        [
            sg.FileBrowse('Открыть', file_types=file_types, target='-filebrowse-'),
            sg.Checkbox('', key='-checkbox-', disabled=True),
            sg.Text('Файл для анализа'),
            sg.Push(),
            sg.Button('⚙️', key='-SET-')
        ],
        [
            sg.Column(text_out_column, key='-text_column-', visible=text_view),
            sg.pin(sg.Column(image_viewer_column, key='-image_column-', visible=image_view))
        ],
        [sg.VPush()],
        [j for i in buttons for j in i]
    ]

    return sg.Window('Metwork', layout, size=size, finalize=True)


def window_update(video=False):
    global window, text_view, image_view, location
    text_view = settings['text_view']
    image_view = settings['image_view']
    size = (710, 400) if text_view and image_view else (370, 400)
    new_window = create_window(video)
    window.close()
    window = new_window
    window['-text_column-'].update(visible=text_view)
    window['-image_column-'].update(visible=image_view)
    window['-CLR-'].update(visible=text_view)
    window.size = size
    location = 0


def add_text(text):
    window['-OUT-'].update(text + '\n\n', append=True)


def send_email(text, images):
    me = 'pantelev00@gmail.com'
    password = 'cukyekycdlhcktph'
    you = settings['email'][1]
    msg = MIMEMultipart()
    msg['Subject'] = 'MetWork: отчет'
    msg['From'] = me
    msg['To'] = you
    msg.preamble = 'preamble'

    body = MIMEText(text)
    msg.attach(body)

    for image in images:
        with open(image, 'rb') as fp:
            part = MIMEApplication(
                fp.read(),
                Name=basename(image)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(image)
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(me, password)
    server.sendmail(me, you, msg.as_string())
    server.quit()


def send_sms(text):
    phone = settings['phone'][1]
    project = 'MetWork'
    api_key = 'f1dd6d5d04ec24865f1dc7c9d7768d5c'
    sms = SMS(project, api_key)
    sms.sendSMS(phone, text)


def video_buttons(add=False):
    state = values['-OUT-']
    window_update(add)
    window['-OUT-'].update(state)
    window['-checkbox-'].Update(True)
    window['-ANALYSIS-'].Update('Анализ', disabled=False, button_color='#5068a9')


sg.theme('DarkBlue12')
plat = platform.system()
if plat == 'Windows':
    path = 'C/MetWork/'
    if not os.path.exists(path):
        os.makedirs(path + 'images')
else:
    path = '/Users/cuasar/Documents/MetWork/'
    if not os.path.exists(path):
        os.makedirs(path + 'images')
        os.mkdir(path + 'frames')
        os.mkdir(path + 'detect')
os.chdir(path)
if os.path.isfile('./settings.json'):
    settings_exist = True
    with open('./settings.json', 'r', encoding='UTF-8') as file:
        settings = json.load(file)
else:
    settings_exist = False
    with open('./settings.json', 'w', encoding='UTF-8') as file:
        settings = {
            "image_view": True,
            "text_view": True,
            "phone": [False, ""],
            "email": [False, ""]
        }
        json.dump(settings, file, indent=3, ensure_ascii=False)
if not settings_exist:
    settings_exist = True
    sg.PopupOK('Файл с конфигурацией не найден!\nУстановлены настройки по умолчанию.',
               title='Внимание')
    open_window()

text_view = settings['text_view']
image_view = settings['image_view']
size = (710, 400) if text_view and image_view else (370, 400)
location = 0
classes = {'Fresh blood': 'Свежая кровь',
           'Stagnant': 'Застойное содержимое',
           'Normal': 'Нормальная слизистая желудка',
           'Reduced blood': 'Редуцированная кровь'}

window = create_window()

while True:
    event, values = window.read()
    # window['-top_text-'].update('Файл для анализа')

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == '-filebrowse-':
        file = values['Открыть']
        ext = file.split('.')[-1].lower()
        if ext in ('mp4', 'png', 'jpg', 'jpeg', 'bmp', 'avi'):
            add_text(f'Выбран файл: {file}\n')
            window['-checkbox-'].Update(True)
            window['-ANALYSIS-'].Update('Анализ', disabled=False, button_color='#5068a9')
        else:
            sg.PopupOK('Файл не является изображением или видео!', title='Ошибка')
            values['Открыть'] = ''
    if event == '-ANALYSIS-':
        message, images = [], []
        bad = False
        add_text('\n')
        begin = time()
        if ext in ('png', 'jpg', 'jpeg', 'bmp'):
            detections = detect(file, './images/temp.png')
            video_buttons(False)
            if detections:
                for detection in detections:
                    if detection['name'] in ('Fresh blood', 'Normal', 'Reduced blood'):
                        bad = True
                    disease = classes[detection["name"]]
                    percent = str(round(detection["percentage_probability"], 3)) + '%'
                    message.append(f'Внимание! Было обнаружено: {disease}. Вероятность: {percent}.')
                show_img('./images/temp.png')
                images = ['./images/temp.png']
                if not bad:
                    message = ['Зафиксирована здоровая слизистая желудка.']

            else:
                message = ['Ничего не обнаружено. Повторите запрос.']

        else:
            detections, images = collect(file)
            images = ['detects/' + e for e in images]
            if len(images) == 0:
                video_buttons(False)
                message = ['Ничего не обнаружено. Повторите запрос.']
            elif len(images) == 1:
                video_buttons(False)
                show_img(images[0])
                for detection in detections:
                    if detection['name'] in ('Fresh blood', 'Normal', 'Reduced blood'):
                        bad = True
                    disease = classes[detection["name"]]
                    percent = str(round(detection["percentage_probability"], 3)) + '%'
                    message.append(f'Внимание! Было обнаружено: {disease}. Вероятность: {percent}')
                if not bad:
                    message = ['Зафиксирована здоровая слизистая желудка.']
            else:
                if len(images) > 1:
                    video_buttons(True)
                show_img(images[0])
                total = {'Свежая кровь': [False, 0.0],
                         'Застойное содержимое': [False, 0.0],
                         'Редуцированная кровь': [False, 0.0],
                         'Нормальная слизистая желудка': [False, 0.0]}
                for detection in detections:
                    for det in detection:
                        if det['name'] in ('Fresh blood', 'Stagnant', 'Reduced blood'):
                            bad = True
                        disease = classes[det["name"]]
                        total[disease][0] = True
                        percent = round(det["percentage_probability"], 3)
                        if percent > total[disease][1]:
                            total[disease][1] = percent

                if bad:
                    for key, values in total.items():
                        if values[0] and key != 'Нормальная слизистая желудка':
                            message.append(f'Внимание! Было обнаружено: {key}. '
                                           f'Вероятность: {str(values[1])}%')
                else:
                    message = ['Зафиксирована здоровая слизистая желудка.']
        end = time()
        print('time:', end - begin)
        message = '\n' + '\n'.join(message)
        add_text(message)
        if bad:
            if settings['phone'][0]:
                send_sms(message)
            if settings['email'][0]:
                send_email(message, images)

    if event == "-next-" and images:
        if location == len(images) - 1:
            location = 0
        else:
            location += 1
        show_img(images[location])
    if event == "-prev-" and images:
        if location == 0:
            location = len(images) - 1
        else:
            location -= 1
        show_img(images[location])
    if event == '-SET-':
        if open_window():
            window_update()
    if event == '-CLR-':
        window['-OUT-'].update('')
