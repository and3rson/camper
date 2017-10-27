var gulp = require('gulp');
var browserify = require('browserify');
var source = require('vinyl-source-stream');
var gutil = require('gulp-util');
var babel = require('gulp-babel');
var connect = require('gulp-connect');

gulp.task('babel', stream => gulp.src('src/*.jsx')
    .pipe(babel({
        presets: ['babel-preset-es2015', 'babel-preset-react']
    }).on('error', function(e) {
        console.error('Error:' + e);
        this.emit('end');
    }))
    .pipe(gulp.dest('./dist'))
);

gulp.task('browserify', () => browserify('./dist/app.js')
    .bundle()
    .pipe(source('bundle.js'))
    .pipe(gulp.dest('./dist/'))
);

gulp.task('connect', () => connect.server({
    port: 9091,
    root: ['views', 'dist', 'static']
}));

gulp.task('build', ['babel', 'browserify']);

gulp.task('watch', () => {
    return gulp.watch('./src/*.jsx', ['build']);
});

gulp.task('default', ['build', 'watch', 'connect']);

