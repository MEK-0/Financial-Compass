package com.garanti.pusula.dto;

import lombok.Data;
import java.util.List;

@Data
public class AnalyzeRequest {
    private RequestPayload payload;

    @Data
    public static class RequestPayload {
        private UserMetadata user_metadata;
        private List<Transaction> transactions;
    }
}