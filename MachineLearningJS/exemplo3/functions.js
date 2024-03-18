/* Functions */

// Function 1
function square(x){
    return x * x;
}

console.log('Function 1')
console.log(square(5)); // 25

// Function 2
function calculateComission(salary){
    return salary * 0.15;
}

var func1comission = calculateComission(2000);
var func2comission = calculateComission(3000);
var func3comission = calculateComission(4000);

console.log('Function 2')
console.log(func1comission, func2comission, func3comission);

// Function 3
function calculateComissionShift(salary, shift){
    var comission = calculateComission(salary);

    if (shift == "Night"){
        console.log('Shift' + shift + ' receives additionals 100. Comission = ' + (comission + 100));
    } else {
        console.log('Shift' + shift + ' receives no additionals. Comission = ' + comission);
    };
}

console.log('Function 3')
calculateComissionShift(2000, "Night");
calculateComissionShift(3000, "Day");
calculateComissionShift(4000, "Night");

// Function 4
function power(base, exponent){
    if (exponent == undefined){
        exponent = 2;
    }

    var result = 1;
    for (var count = 0; count < exponent; count++){
        result *= base;
    }

    return result;
}
console.log('Function 4')
console.log(power(4)); // 16
console.log(power(4, 3)); // 64
console.log(power(4, 0, 2));
console.log(power());

// Function 5
function power2(base, exponent){
    if (exponent == 0){
        return 1;
    } else {
        return base * power2(base, exponent - 1);
    }
}

console.log('Function 5')
console.log(power2(4, 3)); // 64