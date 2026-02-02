import pandas as pd
from app.models.request_models import AnalysisRequest


class DetectiveAgent:
    def __init__(self, data: AnalysisRequest):

        self.df = pd.DataFrame([t.dict() for t in data.transactions])
        self.df['date'] = pd.to_datetime(self.df['date'])

    def detect_subscription_anomalies(self):
        """
        Abonelikler üzerindeki anormallikleri (çift ödeme ve zam) tespit eder.
        """
        alerts = []
        # Sadece SUBSCRIPTION kategorisini süz
        subs = self.df[self.df['category'] == 'SUBSCRIPTION']

        if subs.empty:
            return alerts

        # 1. ÇİFT ABONELİK KONTROLÜ (MCC Bazlı)
        # Aynı MCC koduna (Sektör) sahip farklı açıklamalı işlemleri bul
        mcc_groups = subs.groupby('mcc_code')['description'].unique()
        for mcc, descriptions in mcc_groups.items():
            if len(descriptions) > 1:

                alerts.append({
                    "type": "SUBSCRIPTION_DUPLICATE",
                    "severity": "MEDIUM",
                    "message": f"Aynı harcama grubunda birden fazla abonelik tespit edildi: {', '.join(descriptions)}. Tasarruf için birini iptal etmeyi düşünebilirsiniz.",
                    "potential_savings": float(subs[subs['description'] == descriptions[1]]['amount'].iloc[-1])
                })


        for desc in subs['description'].unique():
            history = subs[subs['description'] == desc].sort_values(by='date')
            if len(history) >= 2:
                last_payment = history.iloc[-1]['amount']
                prev_payment = history.iloc[-2]['amount']

                if last_payment > prev_payment:
                    diff = last_payment - prev_payment
                    hike_perc = (diff / prev_payment) * 100
                    alerts.append({
                        "type": "PRICE_HIKE",
                        "severity": "LOW",
                        "message": f"{desc} abonelik ücretiniz geçen aya göre %{hike_perc:.0f} artmış ({diff:.2f} TL fark).",
                        "potential_savings": float(diff)
                    })

        return alerts