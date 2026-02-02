from app.models.request_models import AnalysisRequest
from app.agents.accountant import AccountantAgent
from app.agents.detective import DetectiveAgent
from datetime import datetime


class FinancialOrchestrator:
    def __init__(self, data: AnalysisRequest):
        self.data = data
        self.accountant = AccountantAgent(data)
        self.detective = DetectiveAgent(data)

    def run_full_analysis(self):

        upcoming_costs = self.accountant.analyze_fixed_costs()
        acc_summary = self.accountant.calculate_summary(upcoming_costs)
        anomalies = self.detective.detect_subscription_anomalies()

        # 2. Kullanıcı İçin Özet Metin (Main'den buraya taşıdık)
        explanation = (
            f"Mevcut {self.data.user_metadata.current_balance} TL bakiyenden, "
            f"{self.data.user_metadata.credit_card_debt} TL kredi kartı borcun ve "
            f"{acc_summary['total_obligations']} TL beklenen faturaların düşülmüştür. "
            f"Maaşına {acc_summary['days_until_salary']} gün kaldı."
        )


        return {
            "analysis_timestamp": datetime.now().isoformat(),
            "safe_to_spend": {
                "amount": acc_summary["safe_to_spend"],
                "explanation": explanation
            },
            "alerts": anomalies,
            "upcoming_obligations": upcoming_costs
        }