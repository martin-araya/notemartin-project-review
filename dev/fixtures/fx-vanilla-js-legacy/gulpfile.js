// gulpfile.js
// Pipeline de build: compila SCSS a CSS y minifica JS a dist/.
// No es necesario para la suite Jest; se usa solo con `npm run build:dist`.
var gulp = require('gulp');
var sass = require('gulp-sass')(require('sass'));
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var fs = require('fs');
var path = require('path');

function clean(done) {
  var dir = path.join(__dirname, 'dist');
  if (fs.existsSync(dir)) {
    fs.rmSync(dir, { recursive: true, force: true });
  }
  done();
}

function styles() {
  return gulp.src('public/scss/main.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('public/css'))
    .pipe(gulp.dest('dist/css'));
}

function scripts() {
  return gulp.src([
    'public/js/app.js',
    'public/js/search.js',
    'public/js/contact.js',
    'public/js/gallery.js',
    'public/js/dispatch.js'
  ])
    .pipe(uglify())
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest('dist/js'));
}

exports.clean = clean;
exports.styles = styles;
exports.scripts = scripts;
exports.default = gulp.series(clean, gulp.parallel(styles, scripts));
