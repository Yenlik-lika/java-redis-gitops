package kz.devops.app;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import redis.clients.jedis.Jedis;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.concurrent.atomic.AtomicLong;

public final class App {
    private static final String VERSION = System.getenv().getOrDefault("APP_VERSION", "v1");
    private static final AtomicLong REQUESTS = new AtomicLong();
    private static final AtomicLong REDIS_ERRORS = new AtomicLong();
    private static final AtomicLong HTTP_500 = new AtomicLong();
    private static final long START = System.currentTimeMillis();

    private App() { }

    /** stdout-қа құрылымды лог жазу: уақыт, деңгей, хабарлама. Kubernetes оны жинайды, Promtail Loki-ге жібереді. */
    static void log(String level, String msg) {
        System.out.println(Instant.now() + " level=" + level + " app=java-redis-app version=" + VERSION + " " + msg);
        System.out.flush();
    }

    public static void main(String[] args) throws Exception {
        String host = System.getenv().getOrDefault("REDIS_HOST", "localhost");
        int port = Integer.parseInt(System.getenv().getOrDefault("REDIS_PORT", "6379"));
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/health", ex -> reply(ex, 200, "OK", "text/plain"));
        server.createContext("/metrics", ex -> reply(ex, 200, metrics(), "text/plain; version=0.0.4"));
        // Әдейі бұзылған эндпоинт: 500 қатесін шақырады және ERROR логын жазады
        server.createContext("/error", ex -> {
            try {
                throw new IllegalStateException("Simulated failure: database connection pool exhausted");
            } catch (IllegalStateException e) {
                HTTP_500.incrementAndGet();
                StringWriter sw = new StringWriter();
                e.printStackTrace(new PrintWriter(sw));
                log("ERROR", "method=GET path=/error status=500 error=\"" + e.getMessage() + "\"");
                System.out.println(sw.toString().trim());
                reply(ex, 500, "Internal Server Error", "text/plain");
            }
        });
        server.createContext("/", ex -> {
            REQUESTS.incrementAndGet();
            try (Jedis jedis = new Jedis(host, port)) {
                long hits = jedis.incr("hits");
                log("INFO", "method=GET path=/ status=200 visits=" + hits);
                reply(ex, 200, "Java+Redis " + VERSION + " | visits: " + hits, "text/plain");
            } catch (Exception e) {
                REDIS_ERRORS.incrementAndGet();
                log("WARN", "method=GET path=/ status=503 error=\"Redis unavailable: " + e.getMessage() + "\"");
                reply(ex, 503, "Redis unavailable", "text/plain");
            }
        });
        server.start();
        log("INFO", "Application started, listening on port 8080");
    }

    /** Prometheus text exposition format. */
    private static String metrics() {
        Runtime rt = Runtime.getRuntime();
        return "# HELP app_info Application version info\n"
            + "# TYPE app_info gauge\n"
            + "app_info{version=\"" + VERSION + "\"} 1\n"
            + "# HELP app_http_requests_total Total HTTP requests to /\n"
            + "# TYPE app_http_requests_total counter\n"
            + "app_http_requests_total " + REQUESTS.get() + "\n"
            + "# HELP app_http_500_total HTTP 500 responses\n"
            + "# TYPE app_http_500_total counter\n"
            + "app_http_500_total " + HTTP_500.get() + "\n"
            + "# HELP app_redis_errors_total Failed Redis calls\n"
            + "# TYPE app_redis_errors_total counter\n"
            + "app_redis_errors_total " + REDIS_ERRORS.get() + "\n"
            + "# HELP app_jvm_memory_used_bytes JVM heap used\n"
            + "# TYPE app_jvm_memory_used_bytes gauge\n"
            + "app_jvm_memory_used_bytes " + (rt.totalMemory() - rt.freeMemory()) + "\n"
            + "# HELP app_uptime_seconds Seconds since start\n"
            + "# TYPE app_uptime_seconds gauge\n"
            + "app_uptime_seconds " + (System.currentTimeMillis() - START) / 1000 + "\n";
    }

    private static void reply(HttpExchange ex, int code, String body, String type) throws IOException {
        byte[] b = body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().set("Content-Type", type);
        ex.sendResponseHeaders(code, b.length);
        try (OutputStream os = ex.getResponseBody()) { os.write(b); }
    }
}
