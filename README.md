<div align="center">

# BiliStreamEcho

Custom AI text-to-speech software based on GPT-SoVITS<br><br>

**English** | [**中文简体**](./docs/cn/README.md)
</div>

---
## Installation

BiliStreamEcho 1.0 integration package
- OneDrive:
- Baidu:

### Windows

If you are a Windows user (tested on win>=10), you can download the integration package directly

### Linux

Untested

### macOS

Untested

### Manual installation

#### Installation dependencies

```bash
pip install -r requirements.txt
```

#### Install FFmpeg

##### Conda users

```bash
conda install ffmpeg
```

##### Ubuntu/Debian users

```bash
sudo apt install ffmpeg
sudo apt install libsox-dev
conda install -c conda-forge 'ffmpeg<7'
```

##### Windows users

Download and place [ffmpeg.exe](https://huggingface.co/lj1995/VoiceConversionWebUI/blob/main/ffmpeg.exe) and [ffprobe.exe](https://huggingface.co/lj1995/VoiceConversionWebUI/blob/main/ffprobe.exe) in the GPT-SoVITS root directory.

## Parameter description

### Home page
- **ID code**: Directly copy the live broadcast room number
- **SESSDATA, bili_jct and buvid3** Get from the web page, related tutorial: https://nemo2011.github.io/bilibili-api/#/get-credential

### Model page

#### Model setting parameters
- **File Path**: Open file path
- **GPT_Model and SoVITS_Model**: Read model files in GPT_weights and SoVITS_weights folders respectively
- **Reference Audio**: Reference audio file path
- **Audio Subtitle**: Reference audio subtitle
- **Reference_Language**: Reference audio language

#### Inference parameters
- **Cutting_Method**: Cutting method
- **Output_Language**: Output language

### Comment page

#### Output text format related variables
- **$USER**: User name
- **$TEXT**: Comment content
- **$COUNT**: Quantity, related to the number of gifts and membership time
- **$GIFT**: Gift name
- **$MEMBER**: Member type

#### Other parameters
- **Punctuation Clear**: After checking, the program will clear the punctuation of the inference text, which will have a certain impact on the inference speed. If there are punctuation inference speed is not ideal or errors are often reported, you can check it.
- **Block Words Filter**: Enter the word in the selection box and click ADD to add it to the blocked word library. Select it in the list below and click DELETE to delete the blocked word.

### About top_p, top_k and temperature
- If you have no experience, just keep the default. These parameters control randomness. The larger the value, the greater the randomness. It is recommended to use the default.
- **top_k** Pick out the top few tokens with the highest probability.
- **top_p** Filter tokens based on top_k.
- **temperature** Control the randomness output.

**Example from GPT-SoVITS document:**
- There are 100 tokens, top_k is set to 5, top_p is set to 0.6, and temperature is set to 0.5.
- Pick out the 5 tokens with the highest probability from the 100 tokens, and the probabilities of these five tokens are (0.3, 0.3, 0.2, 0.2, 0.1).
- Pick out the tokens (0.3 and 0.3) whose cumulative probability does not exceed 0.6, and then randomly pick out a token from these two tokens to output, where the probability of the previous token being selected is higher.

In short, the more random the parameters are, the more repeatable they are, while the lower the parameters are, the more repeatable they are.

## Operation steps
### Start
1. Download the integration package, unzip it and put the project file in a path without a Chinese name
2. Click **BiliStreamEcho.exe** as **administrator** to start the program
3. It is normal that the initial startup is slow. If there is no movement after waiting for a long time, you can close it and click go-mainpage.bat to enter the debugging mode
4. If there is an error, plz let me know
### Connection
1. Open the Chrome browser and log in to the B station account (other browser users, please see: https://nemo2011.github.io/bilibili-api/#/get-credential)
2. Open the developer tools and find the Application tab
3. Find: Storage/Cookies on the left
4. Select any B station domain name, find the corresponding three Values ​​on the right and copy them into the software
5. After entering the live broadcast room code, please click the **Save Settings** button
6. After saving, click Start Server to connect

**Please do not disclose your related values to others, there is a risk of hacking**

**The saved values are stored in the local parameters.json. Please delete the related parameters before sharing with others**

**Don't forget to press Save Settings! It will report an error！**


### TTS model settings
1. Click the **Model** button, and click **File Path** to open the project directory
2. Put the voice model and reference audio in the folder (GPT_weights, SoVITS_weights, example).
3. Click the **Refresh** button or restart the software
4. Select the corresponding model and reference audio file path. (It is recommended to use the audio in the data set, preferably 5 seconds. Reference audio is very important! You will learn the speed and tone, please choose carefully.)
5. Enter the text of the reference audio and the corresponding language.
4. Select the parameters for the text to be synthesized, and pay attention to the corresponding language. It is generally recommended to choose a mixture of Chinese and English, but viewers who encounter Japanese names may not be able to read the names. If you are confident in the performance of your computer, you can choose multiple languages.
5. It is recommended to choose 50 words for segmentation, and do not segment less than 50 words. If an error is reported for 50 words, the video memory is too small, and you can segment by period. If you do not segment, the larger the video memory, the more you can synthesize, but it is easy to synthesize nonsense if the synthesis is too long. The actual test shows that the 4090 graphics card can synthesize about 1,000 words, but even for the 4090, it is recommended to generate in segments.
6. **Click Save Settings. Very important! Don't forget！**

### Comment settings
1. Click the **Comment** button to enter the page
2. I feel that there is nothing much to say about this page. In short, you can turn on/off the corresponding items by checking, and you can customize to add/delete blocked words and change the output format
3. The corresponding parameter description is shown above. The parameters can be deleted in theory. That is to say, originally $USER said: $TEXT. You can delete $USER and only keep $TEXT, so that TTS will not read the audience name when outputting, but only read the content.
3. After setting the parameters, click the **Save Settings** button


## Reference Documents
- **GPT-SoVITS**: https://github.com/RVC-Boss/GPT-SoVITS
- **bilibili-api**: https://github.com/Nemo2011/bilibili-api
- **Some public voice model links**
- ***The integration package comes with Paimeng model and Otto model***
- Mihoyo: https://www.yuque.com/baicaigongchang1145haoyuangong/ib3g1e/nwnaga50cazb2v93
- Mygo: https://www.bilibili.com/video/BV1XH4y137Lk/?spm_id_from=333.337.search-card.all.click&vd_source=4e6fd11ccbcccf162770ae5618e3c76f
- GBC: https://www.bilibili.com/video/BV1gU411o7Ec/?spm_id_from=333.337.search-card.all.click&vd_source=4e6fd11ccbcccf162770ae5618e3c76f 
- - Dong Xuelian: https://www.bilibili.com/video/BV1aQ4y1w7bF/?spm_id_from=3 33.337.search-card.all.click&vd_source=4e6fd11ccbcccf162770ae5618e3c76f