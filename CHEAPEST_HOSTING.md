# Cheapest Hosting Options for Südwest-Energie

Since your website is **dynamic** (requires Python backend), you cannot use free static hosting alone. Here are the most cost-effective options for hosting a Reflex application, ranked by cost and value.

## 1. Hetzner Cloud (VPS) - 🏆 Winner for Value/Performance

**Best for**: Fixed costs, high performance, German data centers (GDPR friendly).

*   **Cost**: ~4.50€ / month (CPX11)
*   **Specs**: 2 vCPU, 2 GB RAM, 40 GB Disk
*   **Pros**:
    *   Extremely cheap for the performance.
    *   Servers in Germany (Falkenstein/Nuremberg).
    *   Full control (root access).
    *   Fixed monthly price (no surprises).
*   **Cons**:
    *   Requires manual setup (Linux administration).
    *   You manage updates/security.
*   **Setup**: Docker + Nginx on Ubuntu.

## 2. Google Cloud Run (Serverless) - 🥈 Winner for Low Traffic

**Best for**: Very low traffic sites, "Set and Forget".

*   **Cost**: ~0€ - 2€ / month (Pay-per-use)
*   **Free Tier**: 2 million requests/month free.
*   **Pros**:
    *   Scales to zero (costs nothing when no one visits).
    *   No server management.
    *   Google infrastructure reliability.
*   **Cons**:
    *   "Cold starts" (first request might take 2-3s).
    *   Costs increase with traffic.
    *   Requires SQL database (Cloud SQL is expensive, ~30€/mo).
    *   *Workaround*: Use SQLite on a volume (cheaper) or a separate cheap VPS for DB.

## 3. Railway / Render (PaaS) - 🥉 Winner for Ease of Use

**Best for**: Developers who don't want to manage servers.

*   **Cost**: ~$5 - $10 / month
*   **Pros**:
    *   Connect GitHub repo -> Auto deploy.
    *   Includes SSL, build pipeline, etc.
    *   Very easy setup.
*   **Cons**:
    *   More expensive than VPS for less power.
    *   US-based companies (check GDPR settings).

---

## 🏆 Recommendation: Hetzner Cloud (CPX11)

For **Südwest-Energie**, a German energy broker, **Hetzner** is the ideal choice:
1.  **German Data Privacy**: Data stays in Germany.
2.  **Professional Performance**: Fast response times.
3.  **Cost**: Unbeatable ~4.50€/month.

### How to deploy on Hetzner (Quick Guide)

1.  **Buy Cloud Server (CPX11)** at [Hetzner Cloud](https://console.hetzner.cloud/).
2.  **SSH into server**: `ssh root@<ip>`
3.  **Install Docker**:
    ```bash
    apt update && apt install docker.io docker-compose -y
    ```
4.  **Copy your project** (git clone).
5.  **Run with Docker Compose**:
    ```bash
    docker-compose up -d --build
    ```
6.  **Setup Domain**: Point A-Record to Server IP.

This gives you a robust, production-ready dynamic website for the price of a coffee.
