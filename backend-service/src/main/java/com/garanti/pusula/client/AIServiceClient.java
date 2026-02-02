package com.garanti.pusula.client;

import com.garanti.pusula.dto.AnalyzeRequest;
import com.garanti.pusula.dto.AnalyzeResponse;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@FeignClient(name = "ai-service", url = "http://localhost:5000")
public interface AIServiceClient {

    @PostMapping("/analyze")
    AnalyzeResponse analyzeData(@RequestBody AnalyzeRequest request);
}