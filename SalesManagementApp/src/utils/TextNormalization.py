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
    
    @staticmethod
    def remove_special_characters_and_Upper(input_string) -> str:
        # Danh sách các ký tự đặc biệt cần loại bỏ
        special_characters = [".", ",", "!", "?", ";", ":", "-", "_", "(", ")", "[", "]", "{", "}", "'", "\"", "/", "\\", "|", "@", "#", "$", "%", "^", "&", "*", "+", "=", "<", ">", "~", "`"]
        
        # Thay thế từng ký tự đặc biệt bằng chuỗi rỗng
        cleaned_string = input_string
        for char in special_characters:
            cleaned_string = cleaned_string.replace(char, "")
        
        # Loại bỏ các khoảng trắng thừa
        cleaned_string = re.sub(r'\s+', ' ', cleaned_string).strip()
        
        result = ""
        for text in cleaned_string.split():
            result += text.capitalize() + " "
        
        return result.strip()
    
    @staticmethod
    def format_number(input_str) -> str:
        input_str = str(input_str).strip()  # Xóa khoảng trắng ở đầu và cuối chuỗi
        # Kiểm tra xem đầu vào có phải là số hay không
        if input_str.isdigit():
            number = int(input_str) # Chuyển đổi chuỗi thành số nguyên
            formatted_number = "{:,}".format(number).replace(",", ".") # Định dạng số với dấu chấm phân cách hàng nghìn
            return formatted_number
        else:
            return input_str
