<?php

use App\Http\Controllers\PropertyController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return response()->json(['app' => 'fx-php-laravel', 'ok' => true]);
});

Route::middleware(['web'])->group(function () {
    // E05: route model binding en la ruta web.
    Route::get('/properties/{property}', [PropertyController::class, 'show'])->name('properties.show.web');

    // S03: ruta dead que apunta a un controller inexistente.
    Route::get('/legacy', 'App\Http\Controllers\LegacyController@index');
});
