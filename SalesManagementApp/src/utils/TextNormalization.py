import re 

class TextNormalization:
    '''
      Class này chứa các phương thức dùng để chuẩn hóa văn bản
    '''
    def __init__(self):
        pass

    @staticmethod
    def remove_special_characters(input_string) -> str:
        """
        Loại bỏ các ký tự đặc biệt trong chuỗi, chỉ giữ lại chữ, số và dấu cách.
        
        Args:
            input_string (str): Chuỗi đầu vào cần làm sạch.
        
        Returns:
            str: Chuỗi đã được làm sạch.
        """
        # Danh sách các ký tự đặc biệt cần loại bỏ
        special_characters = [".", ",", "!", "?", ";", ":", "-", "_", "(", ")", "[", "]", "{", "}", "'", "\"", "/", "\\", "|", "@", "#", "$", "%", "^", "&", "*", "+", "=", "<", ">", "~", "`"]
        
        # Thay thế từng ký tự đặc biệt bằng chuỗi rỗng
        cleaned_string = input_string
        for char in special_characters:
            cleaned_string = cleaned_string.replace(char, "")
        
        # Loại bỏ các khoảng trắng thừa
        cleaned_string = re.sub(r'\s+', ' ', cleaned_string).strip()
        
        return cleaned_string.capitalize()
