package kz.devops.app;

import com.sun.net.httpserver.HttpServer;
import redis.clients.jedis.Jedis;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

public final class App {
    private static final String VERSION = System.getenv().getOrDefault("APP_VERSION", "v1");

    private App() { }

    public static void main(String[] args) throws Exception {
        String host = System.getenv().getOrDefault("REDIS_HOST", "localhost");
        int port = Integer.parseInt(System.getenv().getOrDefault("REDIS_PORT", "6379"));
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/health", ex -> reply(ex, 200, "OK"));
        server.createContext("/", ex -> {
            try (Jedis jedis = new Jedis(host, port)) {
                long hits = jedis.incr("hits");
                reply(ex, 200, "Java+Redis " + VERSION + " | visits: " + hits);
            } catch (Exception e) {
                reply(ex, 503, "Redis unavailable");
            }
        });
        server.start();
        System.out.println("Listening on 8080, version " + VERSION);
    }

    private static void reply(com.sun.net.httpserver.HttpExchange ex, int code, String body)
            throws java.io.IOException {
        byte[] b = body.getBytes(StandardCharsets.UTF_8);
        ex.sendResponseHeaders(code, b.length);
        try (OutputStream os = ex.getResponseBody()) { os.write(b); }
    }
}
