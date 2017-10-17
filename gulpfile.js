var gulp = require('gulp');
var sass = require('gulp-sass');

var config = {
    bootstrapDir: './node_modules/bootstrap-sass',
    bootswatchDir: './node_modules/bootswatch/yeti',
    jqueryDir: './node_modules/jquery/dist/*',
    modernizrDir: './node_modules/modernizr/lib/',
    compileDir: './agrile_frene/static',
    faDir: './node_modules/font-awesome'
};

gulp.task('css', function() {
    return gulp.src(config.compileDir + '/css/app.scss')
    .pipe(sass({
        includePaths: [
            config.bootstrapDir + "/assets/stylesheets",
            config.bootswatchDir, config.faDir + "/scss"],
    }))
    .pipe(gulp.dest(config.compileDir + '/css'));
});

gulp.task('fonts', function() {
    return gulp.src([
        config.bootstrapDir + '/assets/fonts/**/*',
        config.faDir + '/fonts/*'
    ])
    .pipe(gulp.dest(config.compileDir + '/fonts'));
});

gulp.task('js', function() {
    return gulp.src([
        config.bootstrapDir + '/assets/javascripts/**/*',
        config.jqueryDir, config.modernizrDir + "modernizr.js",
        "./node_modules/bootstrap-datepicker/dist/js/*"])
    .pipe(gulp.dest(config.compileDir + '/js'));
});

gulp.task('watch',function() {
    gulp.watch(config.compileDir + "/css/*", ['css']);
});

gulp.task('default', ['css', 'fonts', 'js']);
