module.exports = function (config) {
  config.set({
    basePath: '',
    frameworks: ['jasmine', '@angular-devkit/build-angular'],
    plugins: [
      require('karma-jasmine'),
      require('karma-chrome-launcher'),
      require('karma-coverage'),
      require('@angular-devkit/build-angular/plugins/karma')
    ],
    client: {
      clearContext: false
    },
    coverageReporter: {
      dir: require('path').join(__dirname, '../coverage/frontend'),
      reporters: [
        { type: 'html' },
        { type: 'text-summary' }
      ],
      includeAllSources: true,
      // Inclui todos os arquivos TypeScript da pasta app
      instrumenterOptions: {
        istanbul: { noCompact: true }
      }
    },
    files: [
      // Inclui todos os arquivos .ts da pasta app para cobertura
      { pattern: 'src/app/**/*.ts', included: false, watched: false }
    ],
    reporters: ['progress', 'coverage'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: true,
    browsers: ['Chrome'],
    singleRun: false,
    restartOnFileChange: true
  });
};