import logging
from datetime import datetime
from src.repository.BanHangRepo import BanHangRepo
from src.repository.NhapHangRepo import NhapHangRepo
from src.repository.ChiPhiRepo import ChiPhiRepo

class BaoCaoService:
    def __init__(self):
        logging.info('---BaoCaoService initializing---')
        self.ban_hang_repo = BanHangRepo()
        self.nhap_hang_repo = NhapHangRepo()
        self.chi_phi_repo = ChiPhiRepo()
        
    def report_loi_nhuan(self, month: str, year: str) -> dict:
        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        if month is None or month.strip() == '':
            month = str(now.month)
        if year is None or year.strip() == '':
            year = str(now.year)
        if len(month) == 1:
            month = f'0{month}'
        where_ban_hang = f"strftime('%m-%Y', ngay_ban) = '{month}-{year}'"
        where_nhap_hang = f"strftime('%m-%Y', ngay_nhap) = '{month}-{year}'"
        where_chi_phi = f"strftime('%m-%Y', ngay_tao) = '{month}-{year}'"
        ban_hang = self.ban_hang_repo.report_loi_nhuan(where_ban_hang)
        nhap_hang = self.nhap_hang_repo.report_loi_nhuan(where_nhap_hang)
        chi_phi = self.chi_phi_repo.report_loi_nhuan(where_chi_phi)
        report = {}
        for day in datetime.strptime(f'{year}-{month}-01', '%Y-%m-%d').day:
            report[day] = {
                'ban_hang': 0,
                'nhap_hang': 0,
                'chi_phi': 0
            }
        for item in ban_hang:
            report[datetime.strptime(str(item[1]), '%Y-%m-%d')]['ban_hang'] = item[0]
        for item in nhap_hang:
            report[datetime.strptime(str(item[1]), '%Y-%m-%d')]['nhap_hang'] = item[0]
        for item in chi_phi:
            report[datetime.strptime(str(item[1]), '%Y-%m-%d')]['chi_phi'] = item[0]
        return report
      
    def get_day_month_year(self) -> dict:
        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        return {
            'day': str(now.day),
            'month': str(now.month),
            'year': str(now.year)
        }
        
