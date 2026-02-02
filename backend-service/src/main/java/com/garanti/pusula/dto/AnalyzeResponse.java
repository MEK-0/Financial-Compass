package com.garanti.pusula.dto;

import lombok.Data;
import java.util.List;

@Data
public class AnalyzeResponse {

    // Controller'da setSafe_to_spend dediğin alan bu:
    private SafeToSpend safe_to_spend;

    // Python'dan gelecek diğer alanlar (Şimdilik object yapabiliriz)
    private List<Object> alerts;
    private List<Object> upcoming_obligations;

    // İç içe sınıf (Nested Class)
    @Data
    public static class SafeToSpend {
        private Double amount;
        private String explanation;
    }
}