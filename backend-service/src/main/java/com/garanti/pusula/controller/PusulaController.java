package com.garanti.pusula.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.garanti.pusula.client.AIServiceClient;
import com.garanti.pusula.dto.AnalyzeRequest;   // DTO paketinden geliyor
import com.garanti.pusula.dto.AnalyzeResponse;  // DTO paketinden geliyor
import com.garanti.pusula.dto.Transaction;      // DTO paketinden geliyor
import com.garanti.pusula.dto.UserMetadata;     // DTO paketinden geliyor
import com.garanti.pusula.service.FinancialService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor // @Autowired yerine bunu kullanmak daha modern ve güvenlidir
@CrossOrigin(origins = "*") // Frontend'in her yerden erişmesine izin ver
public class PusulaController {

    private final FinancialService financialService;
    private final AIServiceClient aiServiceClient;

    // JSON verisini konsola yazdırmak için yardımcı araç
    private final ObjectMapper objectMapper = new ObjectMapper();

    @PostMapping(value = "/upload-excel", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public AnalyzeResponse analyzeExcel(
            @RequestParam("file") MultipartFile file,
            @RequestParam("current_balance") Double balance,
            @RequestParam("salary") Double salary) {

        System.out.println("📂 Excel Yükleme İsteği Geldi...");

        // 1. Excel dosyasını oku ve Java listesine çevir
        List<Transaction> transactions = financialService.excelToTransactions(file);
        System.out.println("✅ Excel Okundu. Toplam İşlem Sayısı: " + transactions.size());

        // 2. Kullanıcı bilgilerini (Metadata) hazırla
        UserMetadata metadata = new UserMetadata();
        metadata.setCurrent_balance(balance);
        metadata.setSalary(salary);
        metadata.setCredit_card_debt(0.0); // Varsayılan olarak 0, istersen parametre olarak alabilirsin
        metadata.setSalary_day(1);

        // 3. Python'a gidecek paketi (Request) hazırla
        AnalyzeRequest request = new AnalyzeRequest();
        AnalyzeRequest.RequestPayload payload = new AnalyzeRequest.RequestPayload();
        payload.setUser_metadata(metadata);
        payload.setTransactions(transactions);
        request.setPayload(payload);

        // --- 🔍 JSON KONTROL NOKTASI ---
        // Oluşturduğumuz JSON'ı konsola basıyoruz ki ne gönderdiğimizi görelim.
        try {
            String jsonOutput = objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(request);
            System.out.println("\n🚀 PYTHON'A GÖNDERİLECEK JSON VERİSİ:\n" + jsonOutput + "\n");
        } catch (Exception e) {
            System.out.println("⚠️ JSON yazdırma hatası: " + e.getMessage());
        }

        // 4. Python Servisine Gönder (Hata yakalama mekanizması ile)
        try {
            return aiServiceClient.analyzeData(request);
        } catch (Exception e) {
            System.out.println("⚠️ UYARI: Python servisine ulaşılamadı. (Kapalı olabilir)");
            System.out.println("Hata Detayı: " + e.getMessage());

            // Eğer Python kapalıysa uygulama çökmesin, test amaçlı cevap dönelim.
            return createDummyResponse(balance, transactions.size());
        }
    }

    // Python kapalıyken Swagger'da hata almamak için sahte cevap üreten metot
    private AnalyzeResponse createDummyResponse(Double balance, int transactionCount) {
        AnalyzeResponse response = new AnalyzeResponse();
        AnalyzeResponse.SafeToSpend safe = new AnalyzeResponse.SafeToSpend();
        safe.setAmount(balance);
        safe.setExplanation("AI Servisi şu an çevrimdışı (Test Modu). " + transactionCount + " adet işlem başarıyla işlendi ve JSON formatına çevrildi.");
        response.setSafe_to_spend(safe);
        return response;
    }
}