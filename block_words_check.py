import jieba
from config import config

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, content):
        length = len(content)
        for i in range(length):
            node = self.root
            j = i
            while j < length:
                char = content[j]
                if char in node.children:
                    node = node.children[char]
                    if node.is_end_of_word:
                        return True
                else:
                    break
                j += 1
        return False

trie = Trie()  # 全局的Trie实例

def contains_block_words(content, block_words):
    global trie
    # 构建字典树
    if config.parameters_changed:
        trie = Trie()
        for word in block_words:
            trie.insert(word)
        config.parameters_changed = False
        print("Refresh blocked words")
    # 使用 jieba 进行分词
    words = jieba.lcut(content)
    # 合并分词结果
    combined_content = ''.join(words)
    # 检查内容是否包含屏蔽词
    return trie.search(combined_content)

if __name__ == "__main__":
    # 示例数据
    block_words = ['屏蔽词', '屏蔽词2', 'badword', 'blockword']
    content = '这是一个包含badword的句子。'

    # 检查是否包含屏蔽词
    if contains_block_words(content, block_words):
        print("The sentence contains blocked words")
    else:
        print("The sentence does not contain blocked words")

    content = '这是一个包含blockword的句子。'

    # 检查是否包含屏蔽词
    if contains_block_words(content, block_words):
        print("The sentence contains blocked words")
    else:
        print("The sentence does not contain blocked words")

    config.parameters_changed = True
    block_words = ['屏蔽词', '屏蔽词2', 'badword']
    content = '这是一个包含blockword的句子。'

    # 检查是否包含屏蔽词
    if contains_block_words(content, block_words):
        print("The sentence contains blocked words")
    else:
        print("The sentence does not contain blocked words")

    config.parameters_changed = True
    block_words = ['屏蔽词', '屏蔽词2', 'badword', 'blockword']
    content = '这是一个包含屏蔽词1的句子。'

    # 检查是否包含屏蔽词
    if contains_block_words(content, block_words):
        print("The sentence contains blocked words")
    else:
        print("The sentence does not contain blocked words")
