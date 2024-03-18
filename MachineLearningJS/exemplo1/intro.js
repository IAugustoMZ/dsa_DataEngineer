// Introduction to JavaScript

/* Variables */
console.log("Variables");

var name_dog = "Rex";
console.log(name_dog);

var temperature = 25;
console.log(temperature);

/* Data Types */
console.log("Data Types");

// Strings
var name = "John";
console.log(name);

// Numbers
var age = 25;
console.log(age);

// Booleans
var acessed_web = true;
console.log(acessed_web);

// Undefined
var job;
console.log(job);

/* Variable naming conventions */
var _3years = 3;
console.log(_3years);

/* Not allowed */
/* var if = "teste"
/* console.log(if); */

/* Logical Operators 

&& ==> and
|| ==> or
! ==> not
*/

console.log("Logical Operators");

var note1, note2, note3;

note1 = 7;
note2 = 8;
note3 = 6;

console.log("Operator AND");
console.log(true && true);
console.log(true && false);
console.log(false && true);
console.log(false && false);

console.log( ((note1 < note2) && (note2 < note3)) );

console.log("Operator OR");
console.log(true || true);
console.log(true || false);
console.log(false || true);
console.log(false || false);

console.log( !((note1 < note2) || (note2 < note3)) );

/* Conditionals */
console.log("Conditionals");

var gradeStudent1, gradeStudent2;

gradeStudent1 = 7;
gradeStudent2 = 8;

if (gradeStudent1 >= 5 && gradeStudent2 > 5){
    console.log("Approved");
} else {
    console.log("Disapproved");
}

/* Ternary Operator */
console.log("Ternary Operator");
gradeStudent1 >= 5 ? console.log("Approved") : console.log("Disapproved");

/* Loops */
console.log("Loops");

var languages = ["Python", "JavaScript", "Java", "C++", "C#"];

var i;

for (i = 0; i < languages.length; i++){
    console.log(languages[i]);
}
