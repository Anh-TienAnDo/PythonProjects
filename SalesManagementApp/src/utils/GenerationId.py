import random
import string

class GenerationId:
  @staticmethod
  def generate_id(length, prefix):
    return prefix + '_' + ''.join(random.choices(string.ascii_letters + string.digits, k=length))
