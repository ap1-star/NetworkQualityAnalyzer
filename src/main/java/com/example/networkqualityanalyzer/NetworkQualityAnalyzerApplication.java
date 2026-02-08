package com.example.networkqualityanalyzer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class NetworkQualityAnalyzerApplication {

    public static void main(String[] args) {
        SpringApplication.run(NetworkQualityAnalyzerApplication.class, args);
    }
}
