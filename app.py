import os
import openai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env (در رندر از Environment Variables استفاده کن)
load_dotenv()

app = Flask(__name__)

# خواندن کلید API از محیط
openai.api_key = os.getenv("OPENAI_API_KEY")

# در صورت عدم وجود کلید، خطای واضح بده
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY در متغیرهای محیطی تنظیم نشده است!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({'error': 'پیام نمی‌تواند خالی باشد'}), 400

        # ارسال درخواست به OpenAI (مدل gpt-3.5-turbo)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "تو یک دستیار مفید و دوستانه هستی."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({'reply': reply})

    except openai.error.OpenAIError as e:
        # خطاهای مربوط به OpenAI (مثلاً اعتبار کلید)
        return jsonify({'error': f'خطا در ارتباط با هوش مصنوعی: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'خطای ناشناخته: {str(e)}'}), 500

if __name__ == '__main__':
    # برای اجرای محلی (توسعه)
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
