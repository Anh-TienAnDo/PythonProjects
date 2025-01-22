from src.entity.ChiPhiEntity import ChiPhi
from src.repository.ChiPhiRepo import ChiPhiRepo
from src.utils.GenerationId import GenerationId
import logging
from contants import CHI_PHI_SORT_OPTIONS, CHI_PHI_ID_PREFIX, CHI_PHI_ID_LENGTH
from datetime import datetime

class ChiPhiService:
    def __init__(self):
        logging.info('---ChiPhiService initializing---')
        self.chi_phi_repo = ChiPhiRepo()

    def get_all(self, sort: str, day: str, month: str, year: str) -> list[ChiPhi]:
        sort = sort.strip()
        if sort not in self.get_chi_phi_sort_keys() or sort == '' or sort is None:
            sort = 'Tên A-Z'
        sort_by = self.get_chi_phi_sort_by_key(sort)

        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        if month is None or month.strip() == '':
            month = str(now.month)
        if year is None or year.strip() == '':
            year = str(now.year)
        if len(month) == 1:
            month = f'0{month}'
        if day is None or day.strip() == '':
            where = f"strftime('%m-%Y', ngay_tao) = '{month}-{year}'"
        else:
            if len(day) == 1:
                day = f'0{day}'
            where = f"strftime('%d-%m-%Y', ngay_tao) = '{day}-{month}-{year}'"
        return self.chi_phi_repo.get_all(sort_by, where)
        
    def get_by_id(self, chi_phi_id) -> ChiPhi:
        return self.chi_phi_repo.get_by_id(chi_phi_id)

    def create(self, chi_phi: ChiPhi) -> bool:
        while self.chi_phi_repo.check_exist_id(chi_phi.id):
            chi_phi.id = GenerationId.generate_id(CHI_PHI_ID_LENGTH, CHI_PHI_ID_PREFIX)
        return self.chi_phi_repo.create(chi_phi)

    def update(self, chi_phi_id, chi_phi: ChiPhi) -> bool:
        if not self.chi_phi_repo.check_exist_id(chi_phi_id):
            return False
        return self.chi_phi_repo.update(chi_phi_id, chi_phi)
      
    def delete(self, chi_phi_id) -> bool:
        if not self.chi_phi_repo.check_exist_id(chi_phi_id):
            return False
        return self.chi_phi_repo.delete(chi_phi_id)
    
    def get_chi_phi_sort_keys(self):
        return tuple([key for key in CHI_PHI_SORT_OPTIONS.keys()])
    
    def get_chi_phi_sort_by_key(self, sort_key):
        value = CHI_PHI_SORT_OPTIONS.get(sort_key)
        if value is None:
            return CHI_PHI_SORT_OPTIONS.get('Tên A-Z')
        return value
    
    def get_day_month_year(self) -> dict:
        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        return {
            'day': str(now.day),
            'month': str(now.month),
            'year': str(now.year)
        }