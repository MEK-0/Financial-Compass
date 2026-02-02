package com.garanti.pusula.service;

import com.garanti.pusula.dto.Transaction;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Service
public class FinancialService {

    public List<Transaction> excelToTransactions(MultipartFile file) {
        List<Transaction> transactions = new ArrayList<>();

        try (InputStream is = file.getInputStream();
             Workbook workbook = new XSSFWorkbook(is)) {

            Sheet sheet = workbook.getSheetAt(0);
            DataFormatter dataFormatter = new DataFormatter();

            System.out.println("📊 Excel Okuma Başladı. Toplam Satır: " + sheet.getLastRowNum());

            // Başlık satırını (0) atla, 1'den başla
            for (int i = 1; i <= sheet.getLastRowNum(); i++) {
                Row row = sheet.getRow(i);
                if (row == null) continue;

                try {
                    Transaction transaction = new Transaction();
                    transaction.setId(UUID.randomUUID().toString());

                    // --- 1. SÜTUN: TARİH (Date) ---
                    Cell dateCell = row.getCell(0);
                    if (dateCell != null) {
                        if (dateCell.getCellType() == CellType.NUMERIC) {
                            if (DateUtil.isCellDateFormatted(dateCell)) {
                                transaction.setDate(dateCell.getDateCellValue().toInstant()
                                        .atZone(ZoneId.systemDefault()).toLocalDate());
                            }
                        } else {
                            // Tarih metin olarak girildiyse (Örn: "01.02.2026") kurtarmayı dene
                            try {
                                String dateStr = dataFormatter.formatCellValue(dateCell);
                                transaction.setDate(LocalDate.parse(dateStr, DateTimeFormatter.ofPattern("dd.MM.yyyy")));
                            } catch (Exception e) {
                                transaction.setDate(LocalDate.now()); // Kurtaramazsan bugünü ver
                            }
                        }
                    } else {
                        transaction.setDate(LocalDate.now());
                    }

                    // --- 2. SÜTUN: AÇIKLAMA (Description) ---
                    transaction.setDescription(dataFormatter.formatCellValue(row.getCell(1)));

                    // --- 3. SÜTUN: TUTAR (Amount) ---
                    Cell amountCell = row.getCell(2);
                    if (amountCell != null) {
                        if (amountCell.getCellType() == CellType.NUMERIC) {
                            transaction.setAmount(amountCell.getNumericCellValue());
                        } else {
                            // Sayı metin olarak girildiyse (Örn: "1250") dönüştür
                            try {
                                String amountStr = dataFormatter.formatCellValue(amountCell).replace(",", ".");
                                transaction.setAmount(Double.parseDouble(amountStr));
                            } catch (NumberFormatException e) {
                                System.out.println("⚠️ Satır " + i + ": Tutar okunamadı, 0 atanıyor.");
                                transaction.setAmount(0.0);
                            }
                        }
                    } else {
                        transaction.setAmount(0.0);
                    }

                    // --- 4. SÜTUN: KATEGORİ ---
                    String categoryStr = dataFormatter.formatCellValue(row.getCell(3)).trim();
                    try {
                        if (!categoryStr.isEmpty()) {
                            transaction.setCategory(Transaction.Category.valueOf(categoryStr.toUpperCase()));
                        } else {
                            transaction.setCategory(Transaction.Category.OTHER);
                        }
                    } catch (Exception e) {
                        transaction.setCategory(Transaction.Category.OTHER);
                    }

                    transactions.add(transaction);

                } catch (Exception e) {
                    System.out.println("❌ Satır " + i + " okunurken hata oluştu: " + e.getMessage());
                    // Bu satırı atla ama işlemi durdurma
                }
            }

        } catch (IOException e) {
            throw new RuntimeException("Excel dosyası açılamadı: " + e.getMessage());
        }

        return transactions;
    }
}