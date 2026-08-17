# QR Studio

A Flask web app that generates QR codes for links, Wi-Fi networks, emails,
phone numbers, and SMS messages — built from a bare scaffold, one feature a
day, as a self-directed exercise in server-side web development.

## Features

- **Five QR types**: URL/text, Wi-Fi (with hidden-network support), email,
  phone, and SMS
- **Logo overlay** — optionally upload an image to paste in the center of
  the generated code (automatically forces the highest error-correction
  level so it still scans)
- **PNG download** of any generated code
- Server-side validation with clear error messages for incomplete input

## Requirements

- Python 3.8+
- Flask
- `qrcode[pil]` (qrcode generation + Pillow for image handling)
- pytest (only needed to run the test suite)

## Setup

```bash
python3 -m venv qr_env
source qr_env/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

## Running the tests

```bash
pytest
```

Tests cover `build_payload()` — the function responsible for turning
submitted form fields into the raw string that gets encoded, across all
five QR types plus edge cases (missing fields, special characters that
need escaping in the Wi-Fi format, etc).

## How it works

1. The form submits to `/` as a normal POST request.
2. `build_payload()` turns the submitted fields into the string that
   actually gets encoded — a plain URL, or a formatted string like
   `WIFI:T:WPA;S:MyNetwork;P:secret;;` for Wi-Fi.
3. `make_qr_image()` hands that string to the `qrcode` library, which
   renders it as a Pillow image in memory (and pastes in a logo, if one
   was uploaded).
4. The image is embedded directly in the page as a base64 data URI.
5. `/download` regenerates the same image from a query parameter and
   streams it back as a real file via `send_file`.

## Project structure

```
QR-STUDIO/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    └── test_build_payload.py
```

## Known limitations

- The downloaded PNG regenerates from the payload alone, so it won't
  include an uploaded logo — only the in-page preview does.

## Author

Built by [Karan Yadure](https://www.linkedin.com/in/karan-yadure-89465937a/).
