# تمرین اتصال پایتون به Groq API

## اجرای نسخهٔ MCP

مطابق اسلایدهای ۱۵ تا ۱۷، ابزارها به سرور جدا منتقل شده‌اند:

`Agent → MultiServerMCPClient → stdio → FastMCP → tools`

دو ابزار اختصاصی نیز به `add` و `get_weather` اضافه شده‌اند:

- `analyze_text(text, top_k=5)`: تعداد نویسه، واژه، جمله و واژه‌های یکتا و پرتکرار را برمی‌گرداند. حروف فارسی «ی/ک» یکسان‌سازی می‌شوند، نیم‌فاصله حفظ می‌شود و واژه‌های رایج حذف نمی‌شوند. شمارش جمله بر اساس علائم پایان جمله است.
- `analyze_csv(csv_text)`: متن CSV دارای سرستون را دریافت می‌کند و تعداد ردیف‌ها، خانه‌های خالی و کمینه، بیشینه، میانگین و میانهٔ ستون‌های عددی را برمی‌گرداند. ورودی نامعتبر خطا می‌دهد؛ این ابزار فایل محلی را باز نمی‌کند.

هر دو ابزار حداکثر ۱۰۰٬۰۰۰ نویسه ورودی می‌پذیرند و کتابخانهٔ اضافی لازم ندارند.
مثال CSV: `name,score` با ردیف‌های `Ali,18`، `Sara,20` و `Reza,16`؛ میانگین ستون `score` برابر ۱۸ است.
درخواست نمونهٔ `main.py` هر چهار ابزار را فراخوانی می‌کند.

منطق ابزارها در `tools.py`، ثبت ابزارهای MCP در `mcp_server.py` و اتصال عامل در `main.py` قرار دارد.
برای سازگاری با اسلایدها از `mcp<2` و `langchain-mcp-adapters` استفاده می‌شود.
منابع: [MCP SDK v1](https://py.sdk.modelcontextprotocol.io/v1/) و [LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters).

نصب وابستگی‌های جدید:

```powershell
uv sync --python 3.12
# یا
.\.venv\Scripts\python.exe -m pip install -e .
```

آزمون کشف و اجرای ابزارها از طریق MCP، بدون کلید API:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

اجرای عامل با کلید Groq در `.env`:

```powershell
.\.venv\Scripts\python.exe -m basic_agent.main
```

عامل سرور را خودکار با همان مفسر پایتون اجرا می‌کند و ابتدا نام ابزارهای دریافت‌شده را چاپ می‌کند.
برای اجرای مستقل سرور مطابق اسلاید ۱۵:

```powershell
.\.venv\Scripts\python.exe -m basic_agent.mcp_server
```

سرور منتظر پیام‌های پروتکل روی stdin می‌ماند؛ برای پایان `Ctrl+C` بزنید.
سرور به کلید Groq نیاز ندارد و `.env` را بارگذاری نمی‌کند. آب‌وهوا همچنان آزمایشی است.

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
