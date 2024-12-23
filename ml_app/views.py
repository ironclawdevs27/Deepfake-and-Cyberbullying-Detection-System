from transformers import BertTokenizer, BertModel
import pandas as pd
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
import emoji
import re
from django.shortcuts import render, redirect
import torch
from torchvision import transforms, models
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import face_recognition
from torch.autograd import Variable
import time
from torch import nn
import glob
from torchvision import models
import shutil
from PIL import Image as pImage
import time
from django.conf import settings
from .forms import VideoUploadForm

index_template_name = 'index.html'
predict_template_name = 'predict.html'
about_template_name = 'about.html'

im_size = 112
mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]
sm = nn.Softmax()
inv_normalize = transforms.Normalize(
    mean=-1*np.divide(mean, std), std=np.divide([1, 1, 1], std))
if torch.cuda.is_available():
    device = 'gpu'
else:
    device = 'cpu'

train_transforms = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((im_size, im_size)),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)])


class Model(nn.Module):
    def __init__(self, num_classes, latent_dim=2048, lstm_layers=1, hidden_dim=2048, bidirectional=False):
        super(Model, self).__init__()
        model = models.resnext50_32x4d(pretrained=True)
        self.model = nn.Sequential(*list(model.children())[:-2])
        self.lstm = nn.LSTM(latent_dim, hidden_dim,
                            lstm_layers,  bidirectional)
        self.relu = nn.LeakyReLU()
        self.dp = nn.Dropout(0.4)
        self.linear1 = nn.Linear(2048, num_classes)
        self.avgpool = nn.AdaptiveAvgPool2d(1)

    def forward(self, x):
        batch_size, seq_length, c, h, w = x.shape
        x = x.view(batch_size * seq_length, c, h, w)
        fmap = self.model(x)
        x = self.avgpool(fmap)
        x = x.view(batch_size, seq_length, 2048)
        x_lstm, _ = self.lstm(x, None)
        return fmap, self.dp(self.linear1(x_lstm[:, -1, :]))


class validation_dataset(Dataset):
    def __init__(self, video_names, sequence_length=60, transform=None):
        self.video_names = video_names
        self.transform = transform
        self.count = sequence_length

    def __len__(self):
        return len(self.video_names)

    def __getitem__(self, idx):
        video_path = self.video_names[idx]
        frames = []
        a = int(100/self.count)
        first_frame = np.random.randint(0, a)
        for i, frame in enumerate(self.frame_extract(video_path)):
            faces = face_recognition.face_locations(frame)
            try:
                top, right, bottom, left = faces[0]
                frame = frame[top:bottom, left:right, :]
            except:
                pass
            frames.append(self.transform(frame))
            if (len(frames) == self.count):
                break
        frames = torch.stack(frames)
        frames = frames[:self.count]
        return frames.unsqueeze(0)

    def frame_extract(self, path):
        vidObj = cv2.VideoCapture(path)
        success = 1
        while success:
            success, image = vidObj.read()
            if success:
                yield image


def im_convert(tensor, video_file_name):
    image = tensor.to("cpu").clone().detach()
    image = image.squeeze()
    image = inv_normalize(image)
    image = image.numpy()
    image = image.transpose(1, 2, 0)
    image = image.clip(0, 1)
    return image


def im_plot(tensor):
    image = tensor.cpu().numpy().transpose(1, 2, 0)
    b, g, r = cv2.split(image)
    image = cv2.merge((r, g, b))
    image = image*[0.22803, 0.22145, 0.216989] + [0.43216, 0.394666, 0.37645]
    image = image*255.0
    plt.imshow(image.astype('uint8'))
    plt.show()


def predict(model, img, path='./', video_file_name=""):
    fmap, logits = model(img.to(device))
    img = im_convert(img[:, -1, :, :, :], video_file_name)
    params = list(model.parameters())
    weight_softmax = model.linear1.weight.detach().cpu().numpy()
    logits = sm(logits)
    _, prediction = torch.max(logits, 1)
    confidence = logits[:, int(prediction.item())].item()*100
    print('confidence of prediction:',
          logits[:, int(prediction.item())].item()*100)
    return [int(prediction.item()), confidence]


def plot_heat_map(i, model, img, path='./', video_file_name=''):
    fmap, logits = model(img.to(device))
    params = list(model.parameters())
    weight_softmax = model.linear1.weight.detach().cpu().numpy()
    logits = sm(logits)
    _, prediction = torch.max(logits, 1)
    idx = np.argmax(logits.detach().cpu().numpy())
    bz, nc, h, w = fmap.shape
    out = np.dot(fmap[i].detach().cpu().numpy().reshape(
        (nc, h*w)).T, weight_softmax[idx, :].T)
    predict = out.reshape(h, w)
    predict = predict - np.min(predict)
    predict_img = predict / np.max(predict)
    predict_img = np.uint8(255*predict_img)
    out = cv2.resize(predict_img, (im_size, im_size))
    heatmap = cv2.applyColorMap(out, cv2.COLORMAP_JET)
    img = im_convert(img[:, -1, :, :, :], video_file_name)
    result = heatmap * 0.5 + img*0.8*255
    heatmap_name = video_file_name+"_heatmap_"+str(i)+".png"
    image_name = os.path.join(settings.PROJECT_DIR,
                              'uploaded_images', heatmap_name)
    cv2.imwrite(image_name, result)
    result1 = heatmap * 0.5/255 + img*0.8
    r, g, b = cv2.split(result1)
    result1 = cv2.merge((r, g, b))
    return image_name


def get_accurate_model(sequence_length):
    model_name = []
    sequence_model = []
    final_model = ""
    list_models = glob.glob(os.path.join(
        settings.PROJECT_DIR, "models", "*.pt"))
    for model_path in list_models:
        model_name.append(os.path.basename(model_path))
    for model_filename in model_name:
        try:
            seq = model_filename.split("_")[3]
            if int(seq) == sequence_length:
                sequence_model.append(model_filename)
        except IndexError:
            pass
    if len(sequence_model) > 1:
        accuracy = []
        for filename in sequence_model:
            acc = filename.split("_")[1]
            accuracy.append(acc)
        max_index = accuracy.index(max(accuracy))
        final_model = os.path.join(
            settings.PROJECT_DIR, "models", sequence_model[max_index])
    elif len(sequence_model) == 1:
        final_model = os.path.join(
            settings.PROJECT_DIR, "models", sequence_model[0])
    else:
        print("No model found for the specified sequence length.")
    return final_model


ALLOWED_VIDEO_EXTENSIONS = set(
    ['mp4', 'gif', 'webm', 'avi', '3gp', 'wmv', 'flv', 'mkv'])


def allowed_video_file(filename):
    if (filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS):
        return True
    else:
        return False


def home(request):
    return render(request, 'home.html')


def index(request):
    home(request)
    if request.method == 'GET':
        video_upload_form = VideoUploadForm()
        if 'file_name' in request.session:
            del request.session['file_name']
        if 'preprocessed_images' in request.session:
            del request.session['preprocessed_images']
        if 'faces_cropped_images' in request.session:
            del request.session['faces_cropped_images']
        return render(request, index_template_name, {"form": video_upload_form})
    else:
        video_upload_form = VideoUploadForm(request.POST, request.FILES)
        if video_upload_form.is_valid():
            video_file = video_upload_form.cleaned_data['upload_video_file']
            video_file_ext = video_file.name.split('.')[-1]
            sequence_length = video_upload_form.cleaned_data['sequence_length']
            video_content_type = video_file.content_type.split('/')[0]
            if video_content_type in settings.CONTENT_TYPES:
                if video_file.size > int(settings.MAX_UPLOAD_SIZE):
                    video_upload_form.add_error(
                        "upload_video_file", "Maximum file size 100 MB")
                    return render(request, index_template_name, {"form": video_upload_form})
            if sequence_length <= 0:
                video_upload_form.add_error(
                    "sequence_length", "Sequence Length must be greater than 0")
                return render(request, index_template_name, {"form": video_upload_form})
            if allowed_video_file(video_file.name) == False:
                video_upload_form.add_error(
                    "upload_video_file", "Only video files are allowed ")
                return render(request, index_template_name, {"form": video_upload_form})
            saved_video_file = 'uploaded_file_' + \
                str(int(time.time()))+"."+video_file_ext
            if settings.DEBUG:
                with open(os.path.join(settings.PROJECT_DIR, 'uploaded_videos', saved_video_file), 'wb') as vFile:
                    shutil.copyfileobj(video_file, vFile)
                request.session['file_name'] = os.path.join(
                    settings.PROJECT_DIR, 'uploaded_videos', saved_video_file)
            else:
                with open(os.path.join(settings.PROJECT_DIR, 'uploaded_videos', 'app', 'uploaded_videos', saved_video_file), 'wb') as vFile:
                    shutil.copyfileobj(video_file, vFile)
                request.session['file_name'] = os.path.join(
                    settings.PROJECT_DIR, 'uploaded_videos', 'app', 'uploaded_videos', saved_video_file)
            request.session['sequence_length'] = sequence_length
            return redirect('ml_app:predict')
        else:
            return render(request, index_template_name, {"form": video_upload_form})


def predict_page(request):
    if request.method == "GET":
        if 'file_name' not in request.session:
            return redirect("ml_app:home")
        if 'file_name' in request.session:
            video_file = request.session['file_name']
        if 'sequence_length' in request.session:
            sequence_length = request.session['sequence_length']
        path_to_videos = [video_file]
        video_file_name = os.path.basename(video_file)
        video_file_name_only = os.path.splitext(video_file_name)[0]
        if not settings.DEBUG:
            production_video_name = os.path.join(
                '/home/app/staticfiles/', video_file_name.split('/')[3])
            print("Production file name", production_video_name)
        else:
            production_video_name = video_file_name
        video_dataset = validation_dataset(
            path_to_videos, sequence_length=sequence_length, transform=train_transforms)
        if (device == "gpu"):
            model = Model(2).cuda()
        else:
            model = Model(2).cpu()
        model_name = os.path.join(
            settings.PROJECT_DIR, 'models', get_accurate_model(sequence_length))
        path_to_model = os.path.join(settings.PROJECT_DIR, model_name)
        model.load_state_dict(torch.load(
            path_to_model, map_location=torch.device('cpu')))
        model.eval()
        start_time = time.time()
        print("<=== | Started Videos Splitting | ===>")
        preprocessed_images = []
        faces_cropped_images = []
        cap = cv2.VideoCapture(video_file)
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
            else:
                break
        cap.release()
        print(f"Number of frames: {len(frames)}")
        padding = 40
        faces_found = 0
        for i in range(sequence_length):
            if i >= len(frames):
                break
            frame = frames[i]
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_name = f"{video_file_name_only}_preprocessed_{i+1}.png"
            image_path = os.path.join(
                settings.PROJECT_DIR, 'uploaded_images', image_name)
            img_rgb = pImage.fromarray(rgb_frame, 'RGB')
            img_rgb.save(image_path)
            preprocessed_images.append(image_name)
            face_locations = face_recognition.face_locations(rgb_frame)
            if len(face_locations) == 0:
                continue
            top, right, bottom, left = face_locations[0]
            frame_face = frame[top - padding:bottom +
                               padding, left - padding:right + padding]
            rgb_face = cv2.cvtColor(frame_face, cv2.COLOR_BGR2RGB)
            img_face_rgb = pImage.fromarray(rgb_face, 'RGB')
            image_name = f"{video_file_name_only}_cropped_faces_{i+1}.png"
            image_path = os.path.join(
                settings.PROJECT_DIR, 'uploaded_images', image_name)
            img_face_rgb.save(image_path)
            faces_found += 1
            faces_cropped_images.append(image_name)
        print("<=== | Videos Splitting and Face Cropping Done | ===>")
        print("--- %s seconds ---" % (time.time() - start_time))
        if faces_found == 0:
            return render(request, 'predict_template_name.html', {"no_faces": True})
        try:
            heatmap_images = []
            output = ""
            confidence = 0.0
            for i in range(len(path_to_videos)):
                print("<=== | Started Prediction | ===>")
                prediction = predict(
                    model, video_dataset[i], './', video_file_name_only)
                confidence = round(prediction[1], 1)
                output = "REAL" if prediction[0] == 1 else "FAKE"
                print("Prediction:",
                      prediction[0], "==", output, "Confidence:", confidence)
                print("<=== | Prediction Done | ===>")
                print("--- %s seconds ---" % (time.time() - start_time))
            context = {
                'preprocessed_images': preprocessed_images,
                'faces_cropped_images': faces_cropped_images,
                'heatmap_images': heatmap_images,
                'original_video': production_video_name,
                'models_location': os.path.join(settings.PROJECT_DIR, 'models'),
                'output': output,
                'confidence': confidence
            }
            if settings.DEBUG:
                return render(request, predict_template_name, context)
            else:
                return render(request, predict_template_name, context)
        except Exception as e:
            print(f"Exception occurred during prediction: {e}")
            return render(request, 'cuda_full.html')


def about(request):
    return render(request, about_template_name)


def handler404(request, exception):
    return render(request, '404.html', status=404)


def cuda_full(request):
    return render(request, 'cuda_full.html')


# Load the trained model for Cyberbullying Detection
CYBERBULLYING_MODEL_PATH = 'models\cyber_bullying_model2.pt'


class Bert_Classifier(torch.nn.Module):
    def __init__(self, freeze_bert=False):
        super(Bert_Classifier, self).__init__()
        n_input = 768
        n_hidden = 50
        n_output = 5
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.classifier = torch.nn.Sequential(
            torch.nn.Linear(n_input, n_hidden),
            torch.nn.ReLU(),
            torch.nn.Linear(n_hidden, n_output)
        )
        if freeze_bert:
            for param in self.bert.parameters():
                param.requires_grad = False

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state_cls = outputs[0][:, 0, :]
        logits = self.classifier(last_hidden_state_cls)
        return logits


# Initialize the model
cyberbullying_model = Bert_Classifier()
cyberbullying_model.load_state_dict(torch.load(
    CYBERBULLYING_MODEL_PATH, map_location='cpu'))
cyberbullying_model.eval()

# Tokenizer for BERT
cyberbullying_tokenizer = BertTokenizer.from_pretrained(
    'bert-base-uncased', do_lower_case=True)

# Helper function to clean text


def clean_text(text):
    text = emoji.replace_emoji(text, replace="")
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.strip().lower()
    return text

# Cyberbullying Detection Views


def cyberbullying_index(request):
    return render(request, 'cyberbullying_index.html')


def cyberbullying_detect(request):
    if request.method == 'POST':
        url = request.POST.get('url', '')
        downloader = YoutubeCommentDownloader()
        comments = downloader.get_comments_from_url(
            url, sort_by=SORT_BY_POPULAR)
        comments_list = [clean_text(comment['text']) for comment in comments]
        comments_list = [
            comment for comment in comments_list if comment.strip()]

        # Tokenize comments
        encoded_comments = cyberbullying_tokenizer.batch_encode_plus(
            comments_list,
            max_length=128,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )
        input_ids = encoded_comments["input_ids"]
        attention_mask = encoded_comments["attention_mask"]

        # Get predictions
        with torch.no_grad():
            logits = cyberbullying_model(input_ids, attention_mask)
            predictions = torch.argmax(logits, dim=1).numpy()

        labels = ["Ethnicity", "Race", "Religion", "Age", "Not Bullying"]
        prediction_list = [{"Comment": comments_list[i],
                            "Category": labels[predictions[i]]} for i in range(len(comments_list))]

        # Convert to DataFrame for rendering
        df = pd.DataFrame(prediction_list)
        return render(request, 'cyberbullying_index.html', {
            'table': df.to_html(classes='table table-bordered', index=False).strip()
        })
    return redirect('cyberbullying_index')