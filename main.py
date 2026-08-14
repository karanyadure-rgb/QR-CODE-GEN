from io import BytesIO
from base64 import b64encode

from flask import Flask, render_template, request ,send_file
import qrcode
from qrcode.constants import ERROR_CORRECT_L,ERROR_CORRECT_H,ERROR_CORRECT_M,ERROR_CORRECT_Q

ECC_MAP={
    "M":ERROR_CORRECT_M,
    "L":ERROR_CORRECT_L,
    "H":ERROR_CORRECT_H,
    "Q":ERROR_CORRECT_Q

}

app= Flask(__name__)

def build_payload(form):

    qr_type=form.get("qr_type","link")

    if qr_type =="link":
        return form.get("link_text","").strip()

    if qr_type == "wifi":
        ssid = form.get("wifi_ssid","").strip()
        if not ssid:
            return ""

        password = form.get("wifi_pass","")
        secuirty = form.get("wifi_sec","WPA")
        hidden = "true" if form.get("wifi_hidden") else "false"

        def escape(value):

            for ch in ("\\",";",",",'"',":"):
                value=value.replace(ch,"\\"+ch)
            return value

        if secuirty == "nopass":
            return f"WIFI:T:nopass;S:{escape(ssid)};H:{hidden};;"
        return f"WIFI:T:{secuirty}:S:{escape(ssid)};P:{escape(password)};H:{hidden};;"

    return ""

def make_qr_image(playload, fg="#0A0B0C", bg="#FFFFFF", ecc="M"):

    qr=qrcode.QRCode(
        version=None,
        error_correction=ECC_MAP.get(ecc, ERROR_CORRECT_M),
        box_size=10,
        border=4,
      )
    qr.add_data(playload)
    qr.make(fit=True)
    img= qr.make_image(fill_color=fg, back_color=bg).convert("RGB")
    return img,qr.version

def image_to_data_url(img):
    buf=BytesIO()
    img.save(buf, format="PNG")
    encoded = b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"

@app.route("/",methods=["GET","POST"])
def index():
    context={
    "qr_type": "link",
    "form_values": {},
    "image_data_url": None,
    "error": None,
    }

    if request.method=="POST":
                                                          
        for key, value in request.form.items():
            print(f"{key}:{value!r}")

        payload = build_payload(request.form)
        print(f"payload= {payload!r}")

        if payload :
            img,version = make_qr_image(payload)
            context["image_data_url"]=image_to_data_url(img)
            context["payload"]=payload

    return render_template("index.html",**context)

@app.route("/download")
def download():
    payload=request.args.get("payload","")
    if not payload:
        return "Missing payload", 400

    img,_=make_qr_image(payload)
    buf=BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=True,
        download_name="qr-code.png"
    )


if __name__ == "__main__":
    app.run(debug=True)