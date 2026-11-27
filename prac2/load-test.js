// 4-кезең. k6 жүктеме сценарийі: 50 виртуалды қолданушы, 3 минут.
// Әдепкі мекенжай localhost:8080 (ingress port-forward). CI-де BASE_URL арқылы беріледі.
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE = __ENV.BASE_URL || 'http://localhost:8080/';

export const options = { vus: 50, duration: '3m' };

export default function () {
  const res = http.get(BASE);
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(0.1);
}
