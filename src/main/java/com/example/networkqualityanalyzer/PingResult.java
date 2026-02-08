package com.example.networkqualityanalyzer;

import java.time.LocalDateTime;

public class PingResult {

    private String host;
    private long latency;
    private String status;
    private LocalDateTime time;

    public PingResult(String host, long latency, String status, LocalDateTime time) {
        this.host = host;
        this.latency = latency;
        this.status = status;
        this.time = time;
    }

    public String getHost() {
        return host;
    }

    public long getLatency() {
        return latency;
    }

    public String getStatus() {
        return status;
    }

    public LocalDateTime getTime() {
        return time;
    }
}
