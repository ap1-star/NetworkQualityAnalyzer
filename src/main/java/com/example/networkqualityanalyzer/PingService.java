package com.example.networkqualityanalyzer;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.net.InetAddress;
import java.time.LocalDateTime;

@Service
public class PingService {

    private PingResult lastResult =
            new PingResult("google.com", -1, "STARTING", LocalDateTime.now());

    @Scheduled(fixedRate = 10000)
    public void pingGoogle() {
        try {
            InetAddress address = InetAddress.getByName("google.com");

            long start = System.nanoTime();
            boolean reachable = address.isReachable(5000);
            long end = System.nanoTime();

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
