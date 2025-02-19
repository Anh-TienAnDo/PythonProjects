from src.entity.ChiPhiEntity import ChiPhi
from src.repository.ChiPhiRepo import ChiPhiRepo
from src.utils.GenerationId import GenerationId
import logging
from contants import CHI_PHI_SORT_OPTIONS, CHI_PHI_ID_PREFIX, CHI_PHI_ID_LENGTH, LIMIT
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from src.utils.Decorator import logger, timer

class ChiPhiService:
    def __init__(self):
        self.chi_phi_repo = ChiPhiRepo()

    @logger('ChiPhiService')
    @timer('ChiPhiService')
    def get_all(self, sort: str, day: str, month: str, year: str, page: str, limit=LIMIT) -> dict:
        try:
            offset = str((int(page) - 1) * int(limit))
            sort = sort.strip()
            if sort == '' or sort is None or sort not in self.get_chi_phi_sort_keys():
                sort = 'Tên A-Z'
            sort_by = self.get_chi_phi_sort_by_key(sort)
            day = day.strip()
            month = month.strip()
            year = year.strip()
            now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
            if month is None or month == '':
                month = str(now.month)
            if year is None or year == '':
                year = str(now.year)
            if len(month) == 1:
                month = f'0{month}'
            if day is None or day == '':
                where = f"strftime('%m-%Y', ngay_tao) = '{month}-{year}'"
            else:
                if len(day) == 1:
                    day = f'0{day}'
                where = f"strftime('%d-%m-%Y', ngay_tao) = '{day}-{month}-{year}'"
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.chi_phi_repo.get_all, sort_by, where, limit, offset),
                            executor.submit(self.chi_phi_repo.calculate_total, where)]
            chi_phi_list, calculate_total = [f.result() for f in futures]
            # chi_phi_list = self.chi_phi_repo.get_all(sort_by=sort_by, where=where, limit=limit, offset=offset)
            # calculate_total = self.chi_phi_repo.calculate_total(where=where)
            return {
                'chi_phi_list': chi_phi_list,
                'total_chi_phi': calculate_total[0] if calculate_total[0] is not None else 0,
                'total_gia_chi_phi': calculate_total[1] if calculate_total[1] is not None else 0
            }
        except Exception as e:
            logging.error("Error get_all: %s", e)
            return {
                'chi_phi_list': [],
                'total_chi_phi': 0,
                'total_gia_chi_phi': 0
            }
       
    @logger('ChiPhiService')
    @timer('ChiPhiService') 
    def get_by_id(self, chi_phi_id) -> ChiPhi:
        return self.chi_phi_repo.get_by_id(chi_phi_id)

    @logger('ChiPhiService')
    @timer('ChiPhiService')
    def create(self, chi_phi: ChiPhi) -> bool:
        try:
            while self.chi_phi_repo.check_exist_id(chi_phi.id):
                chi_phi.id = GenerationId.generate_id(CHI_PHI_ID_LENGTH, CHI_PHI_ID_PREFIX)
            return self.chi_phi_repo.create(chi_phi)
        except Exception as e:
            logging.error("Error create: %s", e)
            return False
        
    @logger('ChiPhiService')
    @timer('ChiPhiService')
    def create_many(self, chi_phi_list: list[ChiPhi]) -> bool:
        try:
            for index, chi_phi in enumerate(chi_phi_list):
                while self.chi_phi_repo.check_exist_id(chi_phi_list[index].id):
                    chi_phi_list[index].id = GenerationId.generate_id(CHI_PHI_ID_LENGTH, CHI_PHI_ID_PREFIX)
            return self.chi_phi_repo.create_many(chi_phi_list)
        except Exception as e:
            logging.error("Error create_many: %s", e)
            return False

    @logger('ChiPhiService')
    @timer('ChiPhiService')
    def update(self, chi_phi_id, chi_phi: ChiPhi) -> bool:
        try:
            # if not self.chi_phi_repo.check_exist_id(chi_phi_id):
            #     return False
            return self.chi_phi_repo.update(chi_phi_id, chi_phi)
        except Exception as e:
            logging.error("Error update: %s", e)
            return False
    
    @logger('ChiPhiService')
    @timer('ChiPhiService')  
    def delete(self, chi_phi_id) -> bool:
        try:
            # if not self.chi_phi_repo.check_exist_id(chi_phi_id):
            #     return False
            return self.chi_phi_repo.delete(chi_phi_id)
        except Exception as e:
            logging.error("Error delete: %s", e)
            return False
    
    def get_chi_phi_sort_keys(self):
        try:
            return tuple([key for key in CHI_PHI_SORT_OPTIONS.keys()])
        except Exception as e:
            logging.error("Error get_chi_phi_sort_keys: %s", e)
            return tuple()
    
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
        
    def to_list_dict(self, chi_phi_list: list[ChiPhi]) -> list[dict]:
        return [chi_phi.to_dict() for chi_phi in chi_phi_list]
    
    @logger('ChiPhiService')
    @timer('ChiPhiService')
    def export_data(self, data: list[ChiPhi]) -> bool:
        from src.utils.Excel import Excel
        excel_util = Excel()
        try:
            path = excel_util.select_folder_export()
            if path is None:
                return False
            path = f'{path}/chi_phi_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
            return excel_util.export_data(path, self.to_list_dict(data)) 
        except Exception as e:
            logging.error(e)
            return False
    
    @logger('ChiPhiService')
    @timer('ChiPhiService')
    def import_chi_phi(self) -> bool:
        from src.utils.Excel import Excel
        excel_util = Excel()
        try:
            path = excel_util.select_file_import()
            if path is None:
                return False
            return excel_util.import_chi_phi(path)
        except Exception as e:
            logging.error(e)
            return False