<?php

use CodeIgniter\Router\RouteCollection;

/**
 * @var RouteCollection $routes
 */
// Only explicitly registered routes may be accessed.
$routes->setAutoRoute(false);

// Public routes.
$routes->group('', static function (RouteCollection $routes): void {
    // Public landing page.
    $routes->get('/', 'Home::index');

    // Authentication pages.
    $routes->get('login', 'Auth\LoginController::index');
    $routes->post('login', 'Auth\LoginController::authenticate');
    $routes->get(
        'system-check/backend',
        'SystemCheck::backend'
    );
});

// Authenticated member routes.
$routes->group('member', ['filter' => 'memberAuth'], static function (RouteCollection $routes): void {
    // Member dashboard.
    $routes->get('dashboard', 'Member\DashboardController::index');

    // Member profile.
    $routes->get('profile', 'Member\ProfileController::index');
});

// Administrative routes with a separate authorization filter.
$routes->group('admin', ['filter' => 'adminAuth'], static function (RouteCollection $routes): void {
    // Administrative dashboard.
    $routes->get('dashboard', 'Admin\DashboardController::index');
});
