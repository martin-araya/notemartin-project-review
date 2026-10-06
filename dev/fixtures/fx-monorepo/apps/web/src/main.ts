// Minimal shim of Angular bootstrapping. In a real Angular project, the
// ``bootstrapApplication`` call comes from ``@angular/platform-browser``.
// This file is the entry point referenced by ``angular.json``.

import { AppComponent } from './app/app.component.js';
import { appConfig } from './app/app.config.js';

// ``bootstrapApplication`` is injected at build time by Angular CLI.
// In the fixture we only verify that the module graph compiles, not that
// the runtime bootstraps in a real browser (no Chromium in CI).
console.log('fx-mono-web bootstrap entry: AppComponent =', AppComponent.name);

export { AppComponent, appConfig };
