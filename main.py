import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def extract_intent_entity(sentence):
    # Tokenization
    words = word_tokenize(sentence)
    # POS tagging
    pos_tags = pos_tag(words)

    # Danh sách các thực thể có thể là cây dù
    entity_keywords = ['cây_dù', 'cây dù màu đỏ']

    # Danh sách các intent có thể có
    intent_keywords = ['mua', 'mua_hàng', 'mua_sắm']

    # Tìm kiếm intent
    intent = None
    for word, tag in pos_tags:
        if word.lower() in intent_keywords:
            intent = word.lower()
            break

    # Tìm kiếm thực thể
    entity = None
    for word in words:
        if word.lower() in entity_keywords:
            entity = word
            break

    return intent, entity

# Sử dụng hàm để trích xuất ý định và thực thể từ câu
sentence = "Tôi muốn mua cây_dù màu đỏ"
intent, entity = extract_intent_entity(sentence)
print("Intent:", intent)
print("Thực thể:", entity)
