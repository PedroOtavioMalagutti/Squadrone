/*
Created on 

@author: Calvin Suzuki de Camargo and Guilherme Soares Silvestre
*/
var opts = {
    angle: -0.07, // The span of the gauge arc
    lineWidth: 0.43, // The line thickness
    radiusScale: 1, // Relative radius
    pointer: {
        length: 0.57, // // Relative to gauge radius
        strokeWidth: 0.057, // The thickness
        color: 'red' // Fill color
    },
    limitMax: true,     // If false, max value increases automatically if value > maxValue
    limitMin: true,     // If true, the min value of the gauge will be fixed
    colorStart: '#000000',   // Colors
    colorStop: '#0554b9',    // just experiment with them
    strokeColor: '#E0E0E0',  // to see which ones work best for you
    generateGradient: true,
    highDpiSupport: true,     // High resolution support
};

function setGauge() {
    var target = document.getElementById('gauge'); // your canvas element
    var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
    gauge.maxValue = 100; // set max gauge value
    gauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
    gauge.animationSpeed = 1; // set animation speed (32 is default value)}

    return gauge
}

function updateGauge(gauge, speed) {
    gauge.set(speed); // set actual value
}
