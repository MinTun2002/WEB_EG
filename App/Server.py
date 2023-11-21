from flask import Flask, render_template, request, send_from_directory, send_file

import pyodbc
app = Flask(__name__)

# Kết nối đến cơ sở dữ liệu (thay đổi thông tin kết nối tùy thuộc vào cơ sở dữ liệu bạn đang sử dụng)
conn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=ACER\MINTUN;'
                      'DATABASE=DB_WEB_ENGLISH;'
                      'Trusted_Connection=yes;')  # Sử dụng Trusted_Connection=yes nếu bạn đang sử dụng xác thực Windows

cursor = conn.cursor()

@app.route('/Vocabulary', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_word = request.form['search_word']
        
        # Thực hiện truy vấn SQL để lấy thông tin từ cơ sở dữ liệu (đoạn code 2)
        cursor.execute(f"SELECT * FROM Vocabulary WHERE EnglishWord = '{search_word}'")
        result = cursor.fetchone()
        
        if result:
            # Chuyển kết quả từ tuple sang dictionary để dễ sử dụng trong template (đoạn code 2)
            result_dict = {
                'EnglishWord': result.EnglishWord,
                'VietnameseDefinition': result.VietnameseDefinition,
                'PartOfSpeech': result.PartOfSpeech,
                'ExampleSentence': result.ExampleSentence
            }
            return render_template('Vocabulary.html', result=result_dict)
        else:
            return render_template('Vocabulary.html', message='Word not found!')
    return render_template('Vocabulary.html')
#Part1
# Truy vấn SQL
query = """
    SELECT 
        Part1.IDPart1,
        QUESTION.IDQuestion,
        QUESTION.LinkQUESTION,
        QUESTION.A AS OptionA,
        QUESTION.B AS OptionB,
        QUESTION.C AS OptionC,
        QUESTION.D AS OptionD,
        QUESTION.ANSWER,
        PICTURE.LinkPicture,
        AUDIO.LinkAudio
    FROM 
        Part1
    JOIN 
        QUESTION ON Part1.IDQUESTION = QUESTION.IDQUESTION
    JOIN 
        PICTURE ON Part1.IDPicture = PICTURE.IDPicture
    JOIN 
        AUDIO ON Part1.IDAudio = AUDIO.IDAudio
    WHERE 
        Part1.IDEXAM = 1 AND QUESTION.IDQUESTION BETWEEN 1001 AND 1006;
"""

# Thực thi truy vấn
cursor.execute(query)

# Lấy tất cả dữ liệu
part1_data = cursor.fetchall()
# Đóng kết nối


for row in part1_data:
    print(row)

@app.route('/Part1')
def index():
    return render_template('Part1.html', part1_data=part1_data)

# Định nghĩa một route để phục vụ file âm thanh
# Định nghĩa một route để phục vụ file âm thanh
@app.route('/get_audio/<filename>', methods=['GET', 'POST'])
def get_audio(filename):
    return send_file( 'D:\WEB_CSDL\WEB_E\App\Audio\\'+filename, mimetype='audio/mp3')

# Định nghĩa một route để phục vụ hình ảnh
@app.route('/get_picture/<filename>')
def get_picture(filename):
    return send_file('D:\WEB_CSDL\WEB_E\App\Picture\\'+filename, mimetype='image/png')

# Route để xử lý việc nộp đáp án (giả sử sử dụng method POST)
answer_query = """
    SELECT QUESTION.IDQuestion, QUESTION.ANSWER
    FROM Part1
    JOIN QUESTION ON Part1.IDQUESTION = QUESTION.IDQUESTION
    WHERE Part1.IDEXAM = 1 AND QUESTION.IDQUESTION BETWEEN 1001 AND 1006;
"""

cursor.execute(answer_query)

# Lấy tất cả đáp án từ kết quả truy vấn
answer_data = dict(cursor.fetchall())

@app.route('/submit_answers', methods=['POST'])
def check_answers(user_answers):
    # Làm việc với dữ liệu đáp án từ người dùng và so sánh với đáp án từ cơ sở dữ liệu
    # Đây chỉ là một ví dụ đơn giản, bạn cần điều chỉnh nó phù hợp với cấu trúc thực tế của dữ liệu của bạn.

    # Kiểm tra từng câu hỏi
    score = 0
    for question_id, user_answer in zip(answer_data.keys(), user_answers):
        correct_answer = answer_data[question_id]
        if user_answer.upper() == correct_answer.upper():
            score += 1

    return score

#Part2
query2 = """
    SELECT 
        Part2.IDPart2,
        QUESTION.IDQuestion,
        Part2.PointPart2,
        QUESTION.LinkQUESTION AS Question_Link,
        QUESTION.A AS Option_A,
        QUESTION.B AS Option_B,
        QUESTION.C AS Option_C,
        QUESTION.D AS Option_D,
        QUESTION.ANSWER AS Correct_Answer,
        AUDIO.LinkAudio AS Audio_Link
    FROM 
        Part2
    JOIN 
        QUESTION ON Part2.IDQUESTION = QUESTION.IDQUESTION
    JOIN 
        AUDIO ON Part2.IDAudio = AUDIO.IDAudio
    WHERE 
        Part2.IDEXAM = 1 AND QUESTION.IDQUESTION BETWEEN 1007 AND 1031;
"""

# Thực thi truy vấn
cursor.execute(query2)

# Lấy tất cả dữ liệu
part2_data = cursor.fetchall()
# Đóng kết nối


for row in part2_data:
    print(row)

@app.route('/Part2')
def index1():
    return render_template('Part2.html', part2_data=part2_data)

#Part3
query3 = """
    SELECT 
        Part3.IDPart3,
        Part3.PointPart3,
        QUESTION.IDQuestion,
        QUESTION.LinkQUESTION AS Question_Link,
        QUESTION.A AS Option_A,
        QUESTION.B AS Option_B,
        QUESTION.C AS Option_C,
        QUESTION.D AS Option_D,
        QUESTION.ANSWER AS Correct_Answer,
        PICTURE.LinkPicture AS Picture_Link,
        AUDIO.LinkAudio AS Audio_Link
    FROM 
        Part3
    JOIN 
        QUESTION ON Part3.IDQUESTION = QUESTION.IDQUESTION
    LEFT JOIN 
        PICTURE ON Part3.IDPicture = PICTURE.IDPicture
    JOIN 
        AUDIO ON Part3.IDAudio = AUDIO.IDAudio
    WHERE 
        Part3.IDEXAM = 1 OR Part3.IDPicture IS NULL  -- Include rows where Part3.IDPicture is NULL
    ORDER BY 
        Part3.IDPart3;
"""

# Thực thi truy vấn
cursor.execute(query3)

# Lấy tất cả dữ liệu
part3_data = cursor.fetchall()
# Đóng kết nối


for row in part3_data:
    print(row)

@app.route('/Part3')
def index2():
    return render_template('Part3.html', part3_data=part3_data)


#Part4
query4 = """
    SELECT 
        Part4.IDPart4,
        Part4.PointPart4,
        QUESTION.IDQuestion,
        QUESTION.LinkQUESTION AS Question_Link,
        QUESTION.A AS Option_A,
        QUESTION.B AS Option_B,
        QUESTION.C AS Option_C,
        QUESTION.D AS Option_D,
        QUESTION.ANSWER AS Correct_Answer,
        PICTURE.LinkPicture AS Picture_Link,
        AUDIO.LinkAudio AS Audio_Link
    FROM 
        Part4
    JOIN 
        QUESTION ON Part4.IDQUESTION = QUESTION.IDQUESTION
    LEFT JOIN 
        PICTURE ON Part4.IDPicture = PICTURE.IDPicture
    JOIN 
        AUDIO ON Part4.IDAudio = AUDIO.IDAudio
    WHERE 
        Part4.IDEXAM = 1 OR Part4.IDPicture IS NULL  -- Include rows where Part3.IDPicture is NULL
    ORDER BY 
        Part4.IDPart4;
"""

# Thực thi truy vấn
cursor.execute(query4)

# Lấy tất cả dữ liệu
part4_data = cursor.fetchall()
# Đóng kết nối


for row in part4_data:
    print(row)

@app.route('/Part4')
def index3():
    return render_template('Part4.html', part4_data=part4_data)

#Part5
query5 = """
    SELECT 
        Part5.IDPart5,
        Part5.PointPart5,
        QUESTION.IDQuestion,
        QUESTION.LinkQUESTION AS Question_Link,
        QUESTION.A AS Option_A,
        QUESTION.B AS Option_B,
        QUESTION.C AS Option_C,
        QUESTION.D AS Option_D,
        QUESTION.ANSWER AS Correct_Answer
    FROM Part5
    JOIN 
        QUESTION ON Part5.IDQUESTION = QUESTION.IDQUESTION
    WHERE 
        Part5.IDEXAM = 1;
"""

# Thực thi truy vấn
cursor.execute(query5)

# Lấy tất cả dữ liệu
part5_data = cursor.fetchall()
# Đóng kết nối


for row in part5_data:
    print(row)

@app.route('/Part5')
def index4():
    return render_template('Part5.html', part5_data=part5_data)

#Part6
query6 = """
    SELECT 
        Part6.IDPart6,
        Part6.PointPart6,
        QUESTION.IDQuestion,
        QUESTION.LinkQUESTION AS Question_Link,
        QUESTION.A AS Option_A,
        QUESTION.B AS Option_B,
        QUESTION.C AS Option_C,
        QUESTION.D AS Option_D,
        QUESTION.ANSWER AS Correct_Answer,
        PICTURE.LinkPicture AS Picture_Link
    FROM 
        Part6
    JOIN 
        QUESTION ON Part6.IDQUESTION = QUESTION.IDQUESTION
    JOIN 
        PICTURE ON Part6.IDPicture = PICTURE.IDPicture
    WHERE 
        Part6.IDEXAM = 1
    ORDER BY IDPart6;
"""

# Thực thi truy vấn
cursor.execute(query6)

# Lấy tất cả dữ liệu
part6_data = cursor.fetchall()
# Đóng kết nối


for row in part6_data:
    print(row)

@app.route('/Part6')
def index5():
    return render_template('Part6.html', part6_data=part6_data)

if __name__ == '__main__':
    app.run(debug=True)