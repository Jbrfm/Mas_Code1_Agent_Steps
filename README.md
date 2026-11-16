# تمرین اتصال پایتون به Groq API

این پروژه با LangChain یک مدل زبانی را به دو ابزار `add` و `get_weather` متصل می‌کند.
ابزار جمع محاسبه واقعی انجام می‌دهد؛ آب‌وهوا داده آزمایشی است و به سرویس هواشناسی وصل نیست.

## اجرای پروژه آماده‌شده در ویندوز

۱. در فایل `.env` کنار این راهنما، کلید Groq خود را پس از `OPENAI_API_KEY=` وارد کنید.
کلید را از https://console.groq.com/keys بگیرید. فایل `.env` در Git نادیده گرفته می‌شود.

۲. از ریشه پروژه در PowerShell اجرا کنید:

```powershell
.\.venv\Scripts\python.exe -m basic_agent.main
```

یا از دستور نصب‌شده استفاده کنید:

```powershell
.\.venv\Scripts\basic-agent.exe
```

خروجی شامل پیام‌ها، نام ابزارهای فراخوانی‌شده، نتیجه جمع `139179` و پاسخ نهایی مدل است.
متن دقیق پاسخ و ترتیب فراخوانی ابزارها ممکن است متفاوت باشد.
اگر کلید خالی باشد، برنامه پیش از ارسال درخواست پیام راهنما می‌دهد.

## محیط مجازی و کتابخانه‌ها

محیط `.venv` کتابخانه‌های پروژه را از بقیه سیستم جدا می‌کند.
در IDE، دستور `Python: Select Interpreter` را باز کنید و مسیر زیر را انتخاب کنید:

```text
.venv\Scripts\python.exe
```

وابستگی‌ها در `pyproject.toml` و نسخه‌های دقیق در `uv.lock` ثبت شده‌اند:

- `langchain`: ساخت Agent
- `langchain-openai`: اتصال به API سازگار با OpenAI در Groq
- `langgraph`: اجرای گردش کار Agent
- `python-dotenv`: خواندن تنظیمات از `.env`

نام متغیر `OPENAI_API_KEY` به دلیل کد پروژه است؛ کلید باید متعلق به Groq باشد.
مدل انتخابی `openai/gpt-oss-20b` است. دسترسی و سهمیه حساب را در کنسول Groq بررسی کنید.

## راه‌اندازی دوباره روی دستگاه دیگر

با نصب Python 3.12 و از ریشه پروژه:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
Copy-Item .env.example .env
```

سپس کلید را در `.env` وارد و برنامه را اجرا کنید.
اگر `uv` نصب دارید، به‌جای دو دستور اول از `uv sync --locked --python 3.12` استفاده کنید.
دستور `pip install -e .` وابستگی‌ها را از `pyproject.toml` نصب می‌کند؛ نسخه‌های قفل‌شده با `uv sync --locked` نصب می‌شوند.

برای تحویل تمرین، کد، فایل وابستگی‌ها، `.env.example` و تصویر اجرای موفق را ارائه کنید.
فایل `.env` حاوی کلید و پوشه‌های `.venv` و `.tools` را تحویل ندهید.

## منابع

- https://console.groq.com/docs/quickstart
- https://console.groq.com/docs/openai
- https://console.groq.com/docs/rate-limits

فایل `basic_tool_call.md` یادداشت تاریخی نسخه اولیه در WSL است؛ برای این نسخه ویندوز از این راهنما استفاده کنید.
