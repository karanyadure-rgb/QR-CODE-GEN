from flask import Flask, render_template, request

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

    raise NotImplementedError

def image_to_data_url(img):

    raise NotImplementedError

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

    return render_template("index.html",**context)

if __name__ == "__main__":
    app.run(debug=True)