const CACHE_NAME = 'focustoma-v4';

const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/pwa.js',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/icons/icon-512-maskable.png',
  '/icons/apple-touch-icon.png',
  '/icons/favicon-32.png',
  '/icons/favicon-16.png',
  '/icons/icon.svg',
  '/screenshots/mobile.png',
  '/screenshots/wide.png',
  'https://cdn.tailwindcss.com',
  'https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Noto+Sans+KR:wght@400;500;600;700&display=swap',
];

function isNavigationRequest(request) {
  return request.mode === 'navigate';
}

function precache(cache) {
  return Promise.allSettled(
    PRECACHE_URLS.map((url) =>
      cache.add(url).catch(() => {
        // 외부 CDN 등 일부 리소스 실패해도 설치는 계속
      }),
    ),
  );
}

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => precache(cache).then(() => self.skipWaiting())),
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))),
      )
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const { request } = event;

  if (isNavigationRequest(request)) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put('/index.html', copy));
          return response;
        })
        .catch(() => caches.match('/index.html').then((cached) => cached || caches.match('/'))),
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((cached) => {
      const networkFetch = fetch(request)
        .then((response) => {
          if (response && response.status === 200) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
          }
          return response;
        })
        .catch(() => cached);

      return cached || networkFetch;
    }),
  );
});
