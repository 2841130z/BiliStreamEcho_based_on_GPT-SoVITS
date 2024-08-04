import sys,os

import torch

#new
import json
from tools.i18n.i18n import I18nAuto
i18n = I18nAuto()
# 初始化路径变量
sovits_path = ""
gpt_path = ""

# 检查参数文件是否存在
if os.path.exists('parameters.json'):
    # 打开并读取参数文件
    with open('parameters.json', 'r') as f:
        parameters = json.load(f)

    # 检查所需参数是否存在于文件中
    if "GPT_Model" in parameters and "SoVITS_Model" in parameters:
        sovits_path = "SoVITS_weights/" + parameters["SoVITS_Model"]
        gpt_path = "GPT_weights/" + parameters["GPT_Model"]
    else:
        print("GPT_Model or SoVITS_Model parameter not found in parameters.json. Using default paths.")
        sovits_path = "SoVITS_weights/otto_e39_s1638.pth"
        gpt_path = "GPT_weights/otto-e10.ckpt"
else:
    # 如果参数文件不存在，使用默认路径
    print("parameters.json file not found. Using default paths.")
    sovits_path = "SoVITS_weights/otto_e39_s1638.pth"
    gpt_path = "GPT_weights/otto-e10.ckpt"
# 打印路径以供验证
print(f"sovits_path: {sovits_path}")
print(f"gpt_path: {gpt_path}")

is_half_str = os.environ.get("is_half", "True")
is_half = True if is_half_str.lower() == 'true' else False
is_share_str = os.environ.get("is_share","False")
is_share= True if is_share_str.lower() == 'true' else False

cnhubert_path = "GPT_SoVITS/pretrained_models/chinese-hubert-base"
bert_path = "GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large"
pretrained_sovits_path = "GPT_SoVITS/pretrained_models/s2G488k.pth"
pretrained_gpt_path = "GPT_SoVITS/pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt"

exp_root = "logs"
python_exec = sys.executable or "python"
if torch.cuda.is_available():
    infer_device = "cuda"
elif torch.backends.mps.is_available():
    infer_device = "mps"
else:
    infer_device = "cpu"

webui_port_main = 9874
webui_port_uvr5 = 9873
webui_port_infer_tts = 9872
webui_port_subfix = 9871

api_port = 9880
list_language = {
    i18n("Chinese"): "中文",
    i18n("English"): "英文",
    i18n("Japanese"): "日文",
    i18n("Chinese and English"): "中英混合",
    i18n("Japanese and English"): "日英混合",
    i18n("Multilingual"): "多语种混合",
}

def load_parameters():
    TTS_par={}
    if os.path.exists('parameters.json'):
        # 打开并读取参数文件
        with open('parameters.json', 'r') as f:
            parameters = json.load(f)
    else:
        parameters = {
            "ID_code": "",
            "SESSDATA": "",
            "bili_jct": "",
            "buvid3": "",
            "GPT_Model": "otto-e10.ckpt",
            "SoVITS_Model": "otto_e39_s1638.pth",
            "refer_wav_path": "example\otto_路上停车的问题太多了啊，所以我现在得做这个市区管理了啊.wav",
            "prompt_text": "路上停车的问题太多了啊，所以我现在得做这个市区管理了啊。",
            "top_k": 5,
            "top_p": 1.0,
            "temperature": 1.0,
            "prompt_language": "Chinese",
            "how_to_cut": "No slice",
            "text_language": "Multilingual",
            "Comment_format": "$USER said: $TEXT.",
            "SC_format": "$USER send a super chat: $TEXT.",
            "gift_format": "Thank you $USER for sending $COUNT $GIFT.",
            "member_format": "$USER renewed $MEMBER for $COUNT months. thank you.",
            "Punctuation_filter": False,
            "Comment_switch": True,
            "SC_switch": True,
            "Gift_switch": True,
            "Member_switch": True,
            "System_language": "English"
        }
    # load parameters
    parameters["prompt_language"] = list_language[parameters["prompt_language"]]
    parameters["text_language"] = list_language[parameters["text_language"]]
    TTS_par = parameters

    return TTS_par

if infer_device == "cuda":
    gpu_name = torch.cuda.get_device_name(0)
    if (
            ("16" in gpu_name and "V100" not in gpu_name.upper())
            or "P40" in gpu_name.upper()
            or "P10" in gpu_name.upper()
            or "1060" in gpu_name
            or "1070" in gpu_name
            or "1080" in gpu_name
    ):
        is_half=False

if(infer_device=="cpu"):is_half=False

class Config:
    def __init__(self):
        self.sovits_path = sovits_path
        self.gpt_path = gpt_path
        self.is_half = is_half

        self.cnhubert_path = cnhubert_path
        self.bert_path = bert_path
        self.pretrained_sovits_path = pretrained_sovits_path
        self.pretrained_gpt_path = pretrained_gpt_path

        self.exp_root = exp_root
        self.python_exec = python_exec
        self.infer_device = infer_device

        self.webui_port_main = webui_port_main
        self.webui_port_uvr5 = webui_port_uvr5
        self.webui_port_infer_tts = webui_port_infer_tts
        self.webui_port_subfix = webui_port_subfix

        self.api_port = api_port

        self.parameters_changed = True
        self.parameters=load_parameters()

config=Config()
