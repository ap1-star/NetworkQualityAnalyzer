# NetworkQualityAnalyzer

A Spring Boot application to monitor network latency using scheduled ping checks.

## 📌 Overview

NetworkQualityAnalyzer is a simple backend application that periodically checks network latency by pinging a host and exposing the latest result through a REST API.

The application demonstrates:

- Spring Boot backend development
- Scheduled tasks using `@Scheduled`
- REST API creation
- Network latency measurement using Java networking APIs
- Maven project structure

---

## ⚙️ Features

- Automatically pings a host every 10 seconds
- Measures network latency in milliseconds
- Stores latest ping result in memory
- Exposes REST endpoint to fetch latest network status
- Simple and lightweight design

---

## 🏗️ Tech Stack

- Java 17
- Spring Boot 3
- Maven
