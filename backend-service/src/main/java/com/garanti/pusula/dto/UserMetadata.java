package com.garanti.pusula.dto;

import lombok.Data;

@Data
public class UserMetadata {
    private Double current_balance;
    private Double salary;
    private Double credit_card_debt;
    private int salary_day;
}