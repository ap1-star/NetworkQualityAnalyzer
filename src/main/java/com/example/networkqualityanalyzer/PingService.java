package com.example.networkqualityanalyzer;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class PingService {

    private PingResult lastResult =
            new PingResult("google.com", -1, "STARTING", LocalDateTime.now());

    @Scheduled(fixedRate = 10000)
    public void pingGoogle() {
        try {
            String host = "https://google.com";

long start = System.nanoTime();

java.net.URL url = new java.net.URL(host);
java.net.HttpURLConnection connection =
        (java.net.HttpURLConnection) url.openConnection();

connection.setConnectTimeout(5000);
connection.setReadTimeout(5000);
connection.setRequestMethod("GET");

int responseCode = connection.getResponseCode();

long end = System.nanoTime();

boolean reachable = (responseCode >= 200 && responseCode < 500);


            if (reachable) {
                long latencyMs = (end - start) / 1_000_000;

                lastResult = new PingResult(
                        "google.com",
                        latencyMs,
                        "REACHABLE",
                        LocalDateTime.now()
                );

                System.out.println("Ping: " + latencyMs + " ms");
            } else {
                lastResult = new PingResult(
                        "google.com",
                        -1,
                        "UNREACHABLE",
                        LocalDateTime.now()
                );
            }

        } catch (Exception e) {
            lastResult = new PingResult(
                    "google.com",
                    -1,
                    "ERROR",
                    LocalDateTime.now()
            );
        }
    }

    public PingResult getLastResult() {
        return lastResult;
    }
}
