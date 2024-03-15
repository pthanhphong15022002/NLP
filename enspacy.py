import spacy
import pyodbc as odbc

# Load mô hình tiếng Anh của spaCy
nlp = spacy.load("en_core_web_md")

SERVER_NAME = r'PTHONG\SQLEXPRESS'
DATABASE_NAME = 'Chatbot'
DRIVER_NAME = 'SQL Server'

# Chuỗi kết nối
conn_str = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
"""

def extract_all_tokens(sentence):
    # Tokenization và POS tagging bằng spaCy
    doc = nlp(sentence)
    
    # Trích xuất tất cả các từ trong câu
    tokens = [token.text for token in doc]
    
    return tokens


def extract_intent_subject_object(sentence):
    # Tokenization và POS tagging bằng spaCy
    doc = nlp(sentence)

# Danh sách các intent và các thực thể có thể có
    intent_keywords = ['buy', 'find', 'order']
    subject_entities = ['product', 'item', 'i']
    object_entities = ['iphone', 'apples', 'price']
    
    # Tìm kiếm intent
    intent = None
    for token in doc:
        if token.text.lower() in intent_keywords:
            intent = token.text.lower()
            break
    
    # Tìm kiếm subject (chủ thể)
    subject = None
    for sub in doc:
        if sub.text.lower() in subject_entities:
            subject = sub.text.lower()
            break
    
    # Tìm kiếm object (đối tượng)
    object_ = None
    for ent in doc:
        if ent.text.lower() in object_entities:
            object_ = ent.text.lower()
            break

    named_entities = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    
    return intent, subject, object_, named_entities

# Sử dụng hàm để trích xuất intent, subject và object từ câu
# sentence = "I want to buy two red apples"

# def extract_named_entities(sentences):
#     # Tokenization và nhận diện thực thể bằng spaCy
#     doc = nlp(sentences)
    
#     # Trích xuất các thực thể có thể là tên riêng
#     named_entities = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    
#     return named_entities

# Ví dụ câu chứa tên riêng
# sentences = "John Wick was the 44th President of the United States."
# named_entities = extract_named_entities(sentences)
# print("Named Entities:", named_entities)

# Nhập câu từ người dùng
sentence = input("Nhập câu của bạn: ")

intent, subject, object_, named_entities = extract_intent_subject_object(sentence)
print("Intent:", intent)
print("Subject:", subject)
print("Object:", object_)
print("Named Entities:", named_entities)

# Sử dụng hàm để trích xuất tất cả các từ từ câu
tokens = extract_all_tokens(sentence)
print("Tokens:", tokens)

# Truy vấn database
try:
    conn = odbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute('SELECT Id, Name, Price FROM Products WHERE Name = ?', (object_,))
    print(f"Danh sách {object_}:")
    for row in cursor.fetchall():
        print(row)
except odbc.Error as e:
    print(f"Error: {e}")

finally:
    # Đóng kết nối
    conn.close()