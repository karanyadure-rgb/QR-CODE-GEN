

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import build_payload


# --- link / text -------------------------------------------------------

def test_link_strips_whitespace():
    form = {"qr_type": "link", "link_text": "  https://example.com  "}
    assert build_payload(form) == "https://example.com"


def test_link_empty_returns_empty_string():
    form = {"qr_type": "link", "link_text": ""}
    assert build_payload(form) == ""


# --- wifi ----------------------------------------------------------------

def test_wifi_basic_wpa_network():
    form = {
        "qr_type": "wifi",
        "wifi_ssid": "HomeNet",
        "wifi_pass": "secret123",
        "wifi_sec": "WPA",
    }
    assert build_payload(form) == "WIFI:T:WPA;S:HomeNet;P:secret123;H:false;;"


def test_wifi_escapes_special_characters():
    # a semicolon, colon, and quote in the SSID/password would break the
    # WIFI: format if left unescaped
    form = {
        "qr_type": "wifi",
        "wifi_ssid": "My;Net",
        "wifi_pass": 'p@ss:w"ord',
        "wifi_sec": "WPA",
    }
    assert build_payload(form) == 'WIFI:T:WPA;S:My\\;Net;P:p@ss\\:w\\"ord;H:false;;'


def test_wifi_open_network_has_no_password_field():
    form = {"qr_type": "wifi", "wifi_ssid": "FreeWifi", "wifi_sec": "nopass"}
    assert build_payload(form) == "WIFI:T:nopass;S:FreeWifi;H:false;;"


def test_wifi_missing_ssid_returns_empty_string():
    form = {"qr_type": "wifi", "wifi_ssid": "", "wifi_sec": "WPA"}
    assert build_payload(form) == ""


def test_wifi_hidden_flag():
    form = {
        "qr_type": "wifi",
        "wifi_ssid": "Hidden",
        "wifi_pass": "x",
        "wifi_sec": "WPA",
        "wifi_hidden": "on",
    }
    assert "H:true" in build_payload(form)


# --- email -----------------------------------------------------------------

def test_email_with_subject_and_body():
    form = {
        "qr_type": "email",
        "email_to": "a@b.com",
        "email_subject": "Hi",
        "email_body": "Hello there",
    }
    assert build_payload(form) == "mailto:a@b.com?subject=Hi&body=Hello%20there"


def test_email_minimal_just_the_address():
    form = {"qr_type": "email", "email_to": "a@b.com"}
    assert build_payload(form) == "mailto:a@b.com"


def test_email_missing_address_returns_empty_string():
    form = {"qr_type": "email", "email_to": ""}
    assert build_payload(form) == ""


# --- phone -----------------------------------------------------------------

def test_phone_basic():
    form = {"qr_type": "phone", "phone_number": "+15551234567"}
    assert build_payload(form) == "tel:+15551234567"


def test_phone_missing_number_returns_empty_string():
    form = {"qr_type": "phone", "phone_number": ""}
    assert build_payload(form) == ""


# --- sms ---------------------------------------------------------------

def test_sms_with_message():
    form = {"qr_type": "sms", "sms_number": "+15551234567", "sms_message": "hey"}
    assert build_payload(form) == "SMSTO:+15551234567:hey"


def test_sms_missing_number_returns_empty_string():
    form = {"qr_type": "sms", "sms_number": ""}
    assert build_payload(form) == ""