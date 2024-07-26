<div align="center">

# BiliStreamEcho_based_on_GPT-SoVITS

A Powerful Few-shot Voice Conversion and Text-to-Speech WebUI.<br><br>


[**English**](../../README.md) | **中文简体**
</div>

---
# 用户指导

## 重要提示
**Apply键一定不要忘记按！**

## 参数说明

### Home 页
- **ID code**：直播房间号直接复制
- **SESSDATA, bili_jct 和 buvid3** 从网页获取，相关教程：[点击这里](#)

### Model 页

#### 模型设置参数
- **File Path**：打开文件路径
- **GPT_Model 和 SoVITS_Model**：分别读取 GPT_weights 和 SoVITS_weights 文件夹中的模型文件
- **Reference Audio**：参考音频文件路径
- **Audio Subtitle**：参考音频的字幕
- **Reference_Language**：参考音频的语言

#### 推理参数
- **Cutting_Method**：切分方法
- **Output_Language**：输出语言

### Comment 页

#### 输出文本格式相关变量
- **$USER**：用户名
- **$TEXT**：评论内容
- **$COUNT**：数量，与礼物数量以及加入会员时间有关
- **$GIFT**：礼物名
- **$MEMBER**：会员类型

#### 其他参数
- **标点符号清除**：勾选后程序会清除推理文本的标点，对推理速度有一定影响。如果有标点推理速度不理想或者经常报错可以勾选。
- **Block Words 筛选**：在选框中输入词汇后点击 ADD 加入屏蔽词库。在下方列表中选中后点击 DELETE 可删除屏蔽词。

## 关于 top_p, top_k 和 temperature
- 没经验的话保持默认即可。这些参数控制随机性，值越大随机性越大，建议默认。
- **top_k** 挑出前几个概率最大的 token。
- **top_p** 在 top_k 基础上筛选 token。
- **temperature** 控制随机性输出。

### 例如：
- 有100个 token，top_k 设为5，top_p 设为0.6，temperature 设为0.5。
- 从100个 token 中挑出5个概率最大的 token，这五个 token 的概率分别是（0.3，0.3，0.2，0.2，0.1）。
- 再挑出累加概率不超过0.6的 token（0.3和0.3），再从这两个 token 中随机挑出一个 token 输出，其中前一个 token 被挑选到的几率更大。

还不理解？参数拉满随机性更大，拉低则重复性更高。

## 操作步骤
1. 在文件夹中放入语音模型。
2. 输入参考音频文件路径，建议使用数据集中的音频，最好为5秒。参考音频很重要！会学习语速和语气，请认真选择。
3. 输入参考音频的文本和对应的语种。
4. 选择要合成文本的参数，注意语种要对应。一般推荐选择中英混合，不过遇到日文名的观众可能会读不出名字。对电脑性能有信心的可以选择多语种。
5. 切分建议选择50字一切，低于50字的不切。如果50字一切报错，则显存太小，可以按句号切分。如果不切，显存越大能合成的越多，但合成过长容易胡言乱语。实测4090显卡大约能合成1000字，但即使是4090也建议切分生成。
6. 回到 Home 页面，输入房间号以及 SESSDATA, bili_jct 和 buvid3 后点击 Start server。

