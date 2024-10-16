
import re


def to_non_accent_vietnamese(str):
    str = re.sub(r'[AÁÀÃẠÂẤẦẪẬĂẮẰẴẶ]', 'A', str)
    str = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', str)
    str = re.sub(r'[EÉÈẼẸÊẾỀỄỆ]', 'E', str)
    str = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', str)
    str = re.sub(r'[IÍÌĨỊ]', 'I', str)
    str = re.sub(r'[ìíịỉĩ]', 'i', str)
    str = re.sub(r'[OÓÒÕỌÔỐỒỖỘƠỚỜỠỢ]', 'O', str)
    str = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', str)
    str = re.sub(r'[UÚÙŨỤƯỨỪỮỰ]', 'U', str)
    str = re.sub(r'[ùúụủũưừứựửữ]', 'u', str)
    str = re.sub(r'[YÝỲỸỴ]', 'Y', str)
    str = re.sub(r'[ỳýỵỷỹ]', 'y', str)
    str = re.sub(r'[Đ]', 'D', str)
    str = re.sub(r'[đ]', 'd', str)
    # Some system encode vietnamese combining accent as individual utf-8 characters
    str = re.sub(r'[\u0300\u0301\u0303\u0309\u0323]', '', str)  # Huyền sắc hỏi ngã nặng
    str = re.sub(r'[\u02C6\u0306\u031B]', '', str)  # Â, Ê, Ă, Ơ, Ư
    return str

def slugify(input):
    # Slugify logic here
    input = to_non_accent_vietnamese(input.strip())
    return re.sub(r'[^a-z0-9]+', '-', input.lower())