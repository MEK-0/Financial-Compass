import pandas as pd
from datetime import datetime, timedelta
from app.models.request_models import AnalysisRequest


class AccountantAgent:
    def __init__(self, data: AnalysisRequest):

        self.df = pd.DataFrame([t.dict() for t in data.transactions])
        self.df['date'] = pd.to_datetime(self.df['date'])


        self.metadata = data.user_metadata

    def analyze_fixed_costs(self):
        """
        FIXED ve UTILITY kategorisindeki harcamaları analiz ederek
        gelecek ay beklenen zorunlu giderleri tahmin eder.
        """
        obligations = self.df[self.df['category'].isin(['FIXED', 'UTILITY'])]
        upcoming = []

        for desc in obligations['description'].unique():
            item_history = obligations[obligations['description'] == desc]
            if not item_history.empty:
                last_payment = item_history.sort_values(by='date', ascending=False).iloc[0]

                # Bir sonraki ödeme tarihini tahmin et (+1 ay)
                predicted_date = last_payment['date'] + pd.DateOffset(months=1)

                upcoming.append({
                    "name": desc,
                    "estimated_date": predicted_date.strftime('%Y-%m-%d'),
                    "estimated_amount": float(last_payment['amount'])
                })
        return upcoming

    def calculate_summary(self, upcoming_obligations):
        """
        V1.1.0: Borç, Maaş ve Gelecek Giderleri hesaba katarak özet çıkarır.
        """
        total_upcoming = sum(item['estimated_amount'] for item in upcoming_obligations)

        # Serbest Bakiye Formülü: Bakiye - (Kredi Borcu + Gelecek Giderler)
        safe_to_spend = self.metadata.current_balance - (self.metadata.credit_card_debt + total_upcoming)

        # Maaşa kalan gün hesabı
        today = datetime.now()
        salary_day = self.metadata.salary_day
        # Basit bir gün hesabı (Mevcut ayın salary_day'i)
        next_salary_date = today.replace(day=salary_day)
        if today.day >= salary_day:
            # Eğer maaş günü geçtiyse bir sonraki ayı hedefle
            next_salary_date = (next_salary_date + pd.DateOffset(months=1))

        days_to_salary = (next_salary_date - today).days

        return {
            "safe_to_spend": max(0, safe_to_spend),
            "total_obligations": total_upcoming,
            "days_until_salary": days_to_salary,
            "debt_ratio": (self.metadata.credit_card_debt / self.metadata.salary) * 100
        }