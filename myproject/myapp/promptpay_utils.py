# myapp/promptpay_utils.py
import libscrc
import qrcode # For generating QR code images
# from PIL import Image # Pillow library, a dependency of qrcode - qrcode handles this
import io # For handling in-memory image data
from typing import Union, Optional

import base64

# --- EMVCo Tag Constants ---
TAG_PAYLOAD_FORMAT_INDICATOR = "00"
TAG_POINT_OF_INITIATION_METHOD = "01"
TAG_MERCHANT_ACCOUNT_INFORMATION = "29"
# Sub-tags for Merchant Account Information (Tag 29 - PromptPay specific context)
SUB_TAG_AID_PROMPTPAY = "00"
SUB_TAG_MOBILE_NUMBER_PROMPTPAY = "01"
SUB_TAG_NATIONAL_ID_PROMPTPAY = "02"
# SUB_TAG_EWALLET_ID_PROMPTPAY = "03" # If using e-Wallet ID

TAG_TRANSACTION_CURRENCY = "53"
TAG_TRANSACTION_AMOUNT = "54"
TAG_COUNTRY_CODE = "58"
TAG_CRC = "63"

# --- Standard Values ---
VALUE_PAYLOAD_FORMAT_INDICATOR = "01"
VALUE_POINT_OF_INITIATION_MULTIPLE = "11" # Static QR for multiple uses
VALUE_POINT_OF_INITIATION_ONETIME = "12"  # QR for one-time use
VALUE_PROMPTPAY_AID = "A000000677010111"
VALUE_COUNTRY_CODE_TH = "TH"
VALUE_CURRENCY_THB = "764"

# --- Fixed Lengths ---
LEN_CRC_VALUE_HEX = "04"

class QRError(Exception):
    pass

class InvalidInputError(QRError):
    pass

def _format_tlv(tag: str, value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"TLV value for tag {tag} must be a string, got {type(value)}.")
    length_str = f"{len(value):02d}"
    return f"{tag}{length_str}{value}"

def calculate_crc(code_string: str) -> str:
    try:
        encoded_string = str.encode(code_string, 'ascii')
    except UnicodeEncodeError:
        raise InvalidInputError("Payload contains non-ASCII characters, which is not supported for CRC calculation.")
    crc_val = libscrc.ccitt_false(encoded_string) # type: ignore
    crc_hex_str = hex(crc_val)[2:].upper()
    return crc_hex_str.rjust(4, '0')

def generate_promptpay_qr_payload(
    mobile: Optional[str] = None,
    nid: Optional[str] = None,
    # ewallet_id: Optional[str] = None, # Add if you plan to support e-wallet ID
    amount: Optional[Union[float, int, str]] = None,
    one_time: bool = True # Default to one-time for payments
) -> str:
    if not mobile and not nid: # and not ewallet_id:
        raise InvalidInputError("Either mobile number, National ID (NID) must be provided.")
    # Add more checks if multiple identifiers are provided

    payload_elements = []
    payload_elements.append(
        _format_tlv(TAG_PAYLOAD_FORMAT_INDICATOR, VALUE_PAYLOAD_FORMAT_INDICATOR)
    )

    initiation_method_value = VALUE_POINT_OF_INITIATION_ONETIME if one_time else VALUE_POINT_OF_INITIATION_MULTIPLE
    payload_elements.append(
        _format_tlv(TAG_POINT_OF_INITIATION_METHOD, initiation_method_value)
    )

    merchant_account_sub_elements = []
    merchant_account_sub_elements.append(_format_tlv(SUB_TAG_AID_PROMPTPAY, VALUE_PROMPTPAY_AID))

    if mobile:
        mobile_cleaned = mobile.strip()
        if not (len(mobile_cleaned) == 10 and mobile_cleaned.isdigit() and mobile_cleaned.startswith('0')):
            raise InvalidInputError("Mobile number must be a 10-digit string starting with 0 (e.g., '0812345678').")
        # PromptPay format for mobile is 0066 then mobile number without leading 0
        formatted_mobile_value = f"00{VALUE_COUNTRY_CODE_TH}{mobile_cleaned[1:]}" # Example: 00TH812345678
        merchant_account_sub_elements.append(
            _format_tlv(SUB_TAG_MOBILE_NUMBER_PROMPTPAY, formatted_mobile_value)
        )
    elif nid:
        nid_cleaned = nid.strip().replace('-', '')
        if not (len(nid_cleaned) == 13 and nid_cleaned.isdigit()):
            raise InvalidInputError("National ID (NID) must be a 13-digit string (e.g., '1234567890123').")
        merchant_account_sub_elements.append(
            _format_tlv(SUB_TAG_NATIONAL_ID_PROMPTPAY, nid_cleaned)
        )
    # elif ewallet_id:
    #     # Add e-wallet ID formatting if needed
    #     pass

    payload_elements.append(
        _format_tlv(TAG_MERCHANT_ACCOUNT_INFORMATION, "".join(merchant_account_sub_elements))
    )

    payload_elements.append(
        _format_tlv(TAG_TRANSACTION_CURRENCY, VALUE_CURRENCY_THB)
    )

    if amount is not None:
        amount_str_eval = str(amount).strip()
        if amount_str_eval:
            try:
                amount_float = float(amount_str_eval)
                if amount_float < 0: # Allow 0 for dynamic QR where amount is entered by payer
                    raise InvalidInputError("Transaction amount cannot be negative.")
                if amount_float > 0: # Only include amount tag if amount is greater than 0
                    formatted_amount_value = f"{amount_float:.2f}"
                    if len(formatted_amount_value) > 13: # Max length for amount is 13
                         raise InvalidInputError("Transaction amount is too large.")
                    payload_elements.append(_format_tlv(TAG_TRANSACTION_AMOUNT, formatted_amount_value))
            except ValueError:
                raise InvalidInputError(f"Invalid amount value: '{amount}'. Must be a number.")

    payload_elements.append(
        _format_tlv(TAG_COUNTRY_CODE, VALUE_COUNTRY_CODE_TH)
    )

    data_for_crc_calculation = "".join(payload_elements)
    string_to_calculate_crc_on = data_for_crc_calculation + TAG_CRC + LEN_CRC_VALUE_HEX
    crc_hex_value = calculate_crc(string_to_calculate_crc_on)
    final_payload_string = string_to_calculate_crc_on + crc_hex_value
    return final_payload_string.upper()

def generate_qr_code_image_base64(payload: str, box_size: int = 6, border: int = 4) -> str:
    """Generates a QR code image and returns it as a base64 encoded string."""
    qr_img_obj = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr_img_obj.add_data(payload)
    qr_img_obj.make(fit=True)
    img = qr_img_obj.make_image(fill_color="black", back_color="white")

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str_base64