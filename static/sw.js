// Service Worker for Adiabatic PWA - Enhanced for FOUC prevention
const CACHE_NAME = 'adiabatic-v1.0.1';
const urlsToCache = [
    '/',
    '/static/css/main.css',
    '/static/js/main.js',
    '/static/images/favicon.ico',
    // Cache main pages to prevent FOUC
    '/catalog/',
    '/products/',
    '/about/',
    '/partners/',
    '/blog/',
    '/contacts/'
];

// Install event
self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function (cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

// Fetch event - Enhanced strategy for FOUC prevention
self.addEventListener('fetch', function (event) {
    // For CSS/JS files, prioritize cache to prevent FOUC
    if (event.request.url.includes('.css') || event.request.url.includes('.js')) {
        event.respondWith(
            caches.match(event.request)
                .then(function (response) {
                    if (response) {
                        // Return cached version immediately
                        return response;
                    }
                    // Fallback to network
                    return fetch(event.request).then(function (networkResponse) {
                        // Cache the response for future use
                        if (networkResponse.status === 200) {
                            const responseClone = networkResponse.clone();
                            caches.open(CACHE_NAME).then(function (cache) {
                                cache.put(event.request, responseClone);
                            });
                        }
                        return networkResponse;
                    });
                })
        );
    } else {
        // For other requests, use network first with cache fallback
        event.respondWith(
            fetch(event.request)
                .then(function (response) {
                    // Cache successful responses
                    if (response.status === 200) {
                        const responseClone = response.clone();
                        caches.open(CACHE_NAME).then(function (cache) {
                            cache.put(event.request, responseClone);
                        });
                    }
                    return response;
                })
                .catch(function () {
                    // Fallback to cache if network fails
                    return caches.match(event.request);
                })
        );
    }
});

// Activate event - clean up old caches
self.addEventListener('activate', function (event) {
    event.waitUntil(
        caches.keys().then(function (cacheNames) {
            return Promise.all(
                cacheNames.map(function (cacheName) {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});