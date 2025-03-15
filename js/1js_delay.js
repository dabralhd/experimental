delay_5s = function () {
    setTimeout(function () {
        console.log('5000 ms passed');
    }, 5000);    
}

console.log('Start');
delay_5s(); // 5 seconds delay

var rateColor = function (color, rating) {
    return Object.assign({}, {color: color, rating: rating});
};