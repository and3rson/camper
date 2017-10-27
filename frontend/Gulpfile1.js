const gulp = require('gulp');
const gutil = require('gulp-util');
const browserify = require('browserify');
const babelify = require('babelify');
const source = require('vinyl-source-stream');

gulp.task('build', () => {
    return browserify({
            entries: './src/app.jsx',
            extensions: ['.jsx'],
            debug: true
        })
        .transform('babelify', {
            presets: ['babel-preset-es2015', 'react'],
            plugins: [] // 'transform-react-jsx']
        })
        .bundle()
        .on('error', function(err){
            gutil.log(gutil.colors.red.bold('[browserify error]'));
            gutil.log(err.message);
            this.emit('end');
        })
        .pipe(source('bundle.js'))
        .pipe(gulp.dest('dist'));
});

gulp.task('watch', ['build'], () => {
    gulp.watch('./src/**/*.jsx', ['build']);
});

gulp.task('default', ['watch']);
