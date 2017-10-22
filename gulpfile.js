var gulp = require('gulp');
var sass = require('gulp-sass');

var config = {
    bootstrap: './node_modules/bootstrap-sass',
    bootswatch: './node_modules/bootswatch/yeti',
    jquery: './node_modules/jquery/dist/*',
    datePicker: '"./node_modules/bootstrap-datepicker/dist/js/*',
    modernizr: './node_modules/modernizr/lib/modernizr.js',
    overlay: './node_modules/gasparesganga-jquery-loading-overlay/src/loadingoverlay.min.js',
    compile: './agrile_frene/static',
    fa: './node_modules/font-awesome'
};

gulp.task('css', function() {
    return gulp.src(config.compile + '/css/app.scss')
    .pipe(sass({
        includePaths: [
            config.bootstrap + "/assets/stylesheets",
            config.bootswatch, config.fa + "/scss"],
    }))
    .pipe(gulp.dest(config.compile + '/css'));
});

gulp.task('fonts', function() {
    return gulp.src([
        config.bootstrap + '/assets/fonts/**/*',
        config.fa + '/fonts/*'
    ])
    .pipe(gulp.dest(config.compile + '/fonts'));
});

gulp.task('js', function() {
    return gulp.src([
        config.bootstrap + '/assets/javascripts/**/*', config.overlay,
        config.jquery, config.modernizr, config.datePicker])
    .pipe(gulp.dest(config.compile + '/js'));
});

gulp.task('watch',function() {
    gulp.watch(config.compile + "/css/*", ['css']);
});

gulp.task('default', ['css', 'fonts', 'js']);
