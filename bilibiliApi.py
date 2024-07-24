from bilibili_api import live, sync, Credential
from PyQt5.QtCore import QObject, pyqtSignal
import logging
import asyncio
from threading import Thread
import pygame
import os
import json
import re
import queue
import time
from typing import Dict, Any
import torch
from io import BytesIO
import soundfile as sf
import concurrent.futures

logging.basicConfig(level=logging.INFO)
from api import handle
from config import config
from block_words_check import contains_block_words
from inference_webui import get_tts_wav

def play_audio(file_path):
    # 初始化 pygame
    pygame.mixer.init()

    # 加载音频文件
    try:
        pygame.mixer.music.load(file_path)
    except pygame.error as e:
        print(f"Unable to load audio file: {e}")
        return

    # 播放音频文件
    pygame.mixer.music.play()

    # 保持播放状态直到播放结束
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # 停止播放并释放资源
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def replace_punctuation_with_spaces(text):
    # 定义一个正则表达式模式，匹配所有标点符号，但不包括最后两位字符
    pattern = r'[^\w\s](?=.{2,}$)'
    # 使用re.sub()方法，将所有匹配的标点符号替换为空格
    cleaned_text = re.sub(pattern, '', text)
    print("replace_punctuation_with_spaces")
    return cleaned_text

def replace_all_punctuation(text):
    # 定义一个正则表达式模式，匹配所有标点符号
    pattern = r'[^\w\s]'
    # 使用re.sub()方法，将所有匹配的标点符号替换为空格
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def remove_text_inside_brackets(text):
    # 定义一个正则表达式模式，匹配方括号内的所有文字，包括方括号本身
    pattern = r'\[.*?\]'
    # 使用re.sub()方法，将所有匹配的部分替换为空字符串
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


class CustomQueue(queue.Queue):
    def __init__(self, maxsize=0):
        super().__init__(maxsize)

    def put(self, item, block=True, timeout=None):
        if self.full():
            if item['type'] == 'danmaku':
                # 找到队列中content最短的danmaku项并将其删除
                shortest_item = min(self.queue,
                                    key=lambda x: len(x['content']) if x['type'] == 'danmaku' else float('inf'))
                if len(item['content']) > len(shortest_item['content']):
                    self.queue.remove(shortest_item)
                    print(f"Removed item: {shortest_item}")
                    super().put(item, block, timeout)
                    print(f"Added item: {item}")
                else:
                    print(f"New item discarded: {item}")
            else:
                # 优先删除先放进去的进程，并且进程判断是上舰＞SC＞礼物
                priority_order = {'guard_buy': 1, 'super_chat': 2, 'gift': 3, 'danmaku': 4}

                # 按优先级和顺序找到最优先删除的项
                removable_items = [x for x in self.queue if x['type'] != 'danmaku']
                if removable_items:
                    highest_priority_item = min(removable_items, key=lambda x: priority_order[x['type']])
                else:
                    highest_priority_item = min(self.queue, key=lambda x: priority_order[x['type']])

                self.queue.remove(highest_priority_item)
                print(f"Removed item: {highest_priority_item}")
                super().put(item, block, timeout)
                print(f"Added item: {item}")
        else:
            super().put(item, block, timeout)

class BilibiliApi(QObject):
    connection_established = pyqtSignal()
    connection_closed = pyqtSignal()

    def __init__(self, SESSDATA, bili_jct, buvid3):
        super().__init__()
        self.credential = Credential(sessdata=SESSDATA,
                                     bili_jct=bili_jct,
                                     buvid3=buvid3)
        self.room = None
        self.loop = None
        self.thread = None
        self.queue = CustomQueue(maxsize=5)
        self.consumer_thread = Thread(target=self.consumer)
        self.consumer_thread.daemon = True
        self.consumer_thread.start()

    def start_connection(self, room_id):
        def run():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

            self.room = live.LiveDanmaku(room_id, credential=self.credential)
            logging.info("Room created and attempting to connect")
            self.connection_established.emit()


            @self.room.on('DANMU_MSG')
            async def on_danmaku(event):
                self.handle_event(event, 'danmaku')

            @self.room.on('SEND_GIFT')
            async def on_gift(event):
                self.handle_event(event, 'gift')

            @self.room.on('SUPER_CHAT_MESSAGE')
            async def on_super_chat(event):
                self.handle_event(event, 'super_chat')

            @self.room.on('GUARD_BUY')
            async def on_guard_buy(event):
                self.handle_event(event, 'guard_buy')

            try:
                self.loop.run_until_complete(self.room.connect())
            finally:
                self.loop.run_until_complete(self.loop.shutdown_asyncgens())
                self.loop.close()

        self.thread = Thread(target=run)
        self.thread.start()

    def handle_event(self, event: Dict[str, Any], event_type: str):
        if event_type == 'danmaku':
            info = event.get('data', {}).get('info', [])
            if info and len(info) > 1:
                content = info[1]
                user_id = info[2][0]
                username = info[2][1]
                text=remove_text_inside_brackets(content)
                text = replace_all_punctuation(text)
                if contains_block_words(content, config.parameters["Block_Words"]):
                    logging.info('BLOCK')
                elif text is None or not text.strip():
                    logging.info("None text")
                else:
                    self.queue.put({
                        'type': 'danmaku',
                        'content': remove_text_inside_brackets(content),
                        'user_id': user_id,
                        'username': username
                    })
                    logging.info("Comment is placed in the queue")

        elif event_type == 'gift':
            info = event['data']['data']
            self.queue.put({
                'type': 'gift',
                'gift_info': {
                    'username': info['uname'],
                    'gift_name': info['giftName'],
                    'gift_num': info['num']
                }
            })
            logging.info("Gift information is placed in the queue")

        elif event_type == 'super_chat':
            info = event['data']['data']
            self.queue.put({
                'type': 'super_chat',
                'super_chat_info': {
                    'username': info['user_info']['uname'],
                    'message': remove_text_inside_brackets(info['message']),
                    'amount': info['price']
                }
            })
            logging.info("Super Chat message is placed in the queue")

        elif event_type == 'guard_buy':
            info = event.get('data', {})

            # 直接使用 info 变量，因为它已经是一个字典
            user_data = info["data"]
            print(user_data)

            try:
                # 确保正确访问嵌套字典中的字段
                username = user_data["username"]
                guard_level = user_data["guard_level"]
                num = user_data["num"]
                gift_name = user_data["gift_name"]

                # 继续处理其他字段...
                #logging.info(f"username: {username}, guard level: {guard_level}, number: {num}, gift name: {gift_name}")

            except KeyError as e:
                logging.error(f"GUARD_BUY ERROR: {e}")

            # 打印接收到的数据，以便调试
            #logging.debug(f"接收到的info数据: {info}")

            if username:
                print(username, num, gift_name)  # 打印字段值以调试
                self.queue.put({
                    'type': 'guard_buy',
                    'guard_info': {
                        'username': username,
                        'guard_level': guard_level,
                        'num': num,
                        'gift_name': gift_name
                    }
                })
                logging.info("Put member information into queue")
            else:
                logging.error(f"GUARD_BUY ERROR")

    def consumer(self):
        while True:
            if not self.queue.empty():
                event = self.queue.get()
                event_type = event['type']
                format_par = config.parameters
                if event_type == 'danmaku':
                    self.process_danmaku(event, format_par)
                elif event_type == 'gift':
                    self.process_gift(event, format_par)
                elif event_type == 'super_chat':
                    self.process_super_chat(event, format_par)
                elif event_type == 'guard_buy':
                    self.process_guard_buy(event, format_par)

                self.queue.task_done()
            time.sleep(0.5)

    def process_danmaku(self, event, format_par):
        content = event['content']
        user_id = event['user_id']
        username = event['username']
        logging.info(f"Processing comment: {content}")
        if "Comment_format" in format_par:
            format_str = format_par["Comment_format"]
            text = re.sub(r'\$USER', username, format_str)
            text = re.sub(r'\$TEXT', content, text)
            if format_par["Punctuation_filter"]:
                text = replace_punctuation_with_spaces(text)
        self.generate_audio(text, format_par)

    def process_gift(self, event, format_par):
        gift_info = event['gift_info']
        logging.info(f"Handling Gifts: {gift_info}")
        if "gift_format" in format_par:
            format_str = format_par["gift_format"]
            text = re.sub(r'\$USER', gift_info['username'], format_str)
            text = re.sub(r'\$COUNT', str(gift_info['gift_num']), text)
            text = re.sub(r'\$GIFT', gift_info['gift_name'], text)
            if format_par["Punctuation_filter"]:
                text = replace_punctuation_with_spaces(text)
        self.generate_audio(text, format_par)

    def process_super_chat(self, event, format_par):
        super_chat_info = event['super_chat_info']
        logging.info(f"Handling Super Chat: {super_chat_info}")
        if "SC_format" in format_par:
            format_str = format_par["SC_format"]
            text = re.sub(r'\$USER', super_chat_info['username'], format_str)
            text = re.sub(r'\$TEXT', super_chat_info['message'], text)
            if format_par["Punctuation_filter"]:
                text = replace_punctuation_with_spaces(text)
        self.generate_audio(text, format_par)

    def process_guard_buy(self, event, format_par):
        guard_info = event['guard_info']
        #guard_level_name = event['guard_level_name']
        logging.info(f"Processing member joining: {guard_info}")
        if "member_format" in format_par:
            format_str = format_par["member_format"]
            text = re.sub(r'\$USER', guard_info['username'], format_str)
            text = re.sub(r'\$COUNT', str(guard_info['num']), text)
            text = re.sub(r'\$MEMBER', guard_info["gift_name"], text)
            if format_par["Punctuation_filter"]:
                text = replace_punctuation_with_spaces(text)
        self.generate_audio(text, format_par)


    def generate_audio(self, text, format_par):
        def _generate_audio_task():
            logging.info("Start TTS")
            with torch.no_grad():
                gen = get_tts_wav(
                    format_par["refer_wav_path"], format_par["prompt_text"], format_par["prompt_language"], text,
                    format_par["text_language"], format_par["how_to_cut"], format_par["top_k"], format_par["top_p"],
                    format_par["temperature"]
                )
                sampling_rate, audio_data = next(gen)

            wav = BytesIO()
            sf.write(wav, audio_data, sampling_rate, format="wav")
            wav_file_path = "temporary_audio.wav"
            with open(wav_file_path, 'wb') as f:
                f.write(wav.getvalue())
            torch.cuda.empty_cache()
            # if device == "mps":
            # print('executed torch.mps.empty_cache()')
            # torch.mps.empty_cache()

        # 使用 ThreadPoolExecutor 来设定超时时间
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(_generate_audio_task)

            try:
                future.result(timeout=15)  # 设定超时时间为15秒
                play_audio("temporary_audio.wav")
            except concurrent.futures.TimeoutError:
                torch.cuda.empty_cache()
                # if device == "mps":
                # print('executed torch.mps.empty_cache()')
                # torch.mps.empty_cache()
                logging.error("The TTS task timed out and was canceled.")


    async def async_stop_connection(self):
        if self.room:
            logging.info("Attempting to disconnect")
            await self.room.disconnect()
            self.room = None
            self.connection_closed.emit()
            logging.info("Disconnected and room set to None")

    def stop_connection(self):
        try:
            # 清空队列
            self.queue.queue.clear()
            logging.info("Queue cleared")

            if self.room and self.loop and self.thread:
                future = asyncio.run_coroutine_threadsafe(self.async_stop_connection(), self.loop)
                future.result()  # 等待协程完成

                logging.info("Cancelling all tasks before stopping the loop")
                pending = [task for task in asyncio.all_tasks(self.loop) if not task.done()]
                for task in pending:
                    task.cancel()
                    try:
                        self.loop.run_until_complete(task)
                    except asyncio.CancelledError:
                        logging.info(f"Task {task} cancelled")

                logging.info("Event loop stop called")
                self.loop.call_soon_threadsafe(self.loop.stop)
                self.thread.join()  # 等待线程结束
                logging.info("Thread joined")


        except Exception as e:
            logging.error(f"ERROR: {e}")



if __name__ == "__main__":
    try:
        BilibiliApi.start_connection()
    except KeyboardInterrupt:
        BilibiliApi.stop_connection()