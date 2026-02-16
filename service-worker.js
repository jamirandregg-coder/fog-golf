const CACHE_NAME = 'fog-golf-v1';
const ASSETS_TO_PRECACHE = [
  '/',
  '/index.html'
];

// Install: pre-cache the HTML shell
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS_TO_PRECACHE))
  );
  self.skipWaiting();
});

// Activate: clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: Network-first strategy
// Try network first (app needs Firebase for all data).
// Fall back to cache for the HTML shell if offline.
// Never cache Firebase/API requests.
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Skip caching for Firebase, EmailJS, and other API/SDK requests
  if (
    url.hostname.includes('firebaseio.com') ||
    url.hostname.includes('emailjs.com') ||
    url.hostname.includes('gstatic.com')
  ) {
    return; // Let the browser handle these normally
  }

  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Clone and cache successful same-origin responses
        if (response.ok && url.origin === self.location.origin) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      })
      .catch(() => {
        // Network failed — serve from cache
        return caches.match(event.request).then(cached => {
          if (cached) return cached;
          // For navigation requests, serve the cached index
          if (event.request.mode === 'navigate') {
            return caches.match('/index.html');
          }
          return new Response('Offline', { status: 503, statusText: 'Offline' });
        });
      })
  );
});
