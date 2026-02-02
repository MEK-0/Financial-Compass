package com.garanti.pusula;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableFeignClients 
public class FinancialCompassApplication {

    public static void main(String[] args) {
        SpringApplication.run(FinancialCompassApplication.class, args);
    }

}