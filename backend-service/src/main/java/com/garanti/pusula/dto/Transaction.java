package com.garanti.pusula.dto;

import lombok.Data;
import java.time.LocalDate;

@Data
public class Transaction {
    private String id;
    private LocalDate date;
    private Double amount;
    private String description;
    private Category category;

    public enum Category {
        FIXED, SUBSCRIPTION, LIFESTYLE, UTILITY, OTHER
    }
}