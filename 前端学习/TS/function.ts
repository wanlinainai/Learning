// function hello(txt: string): void {
//   console.log('function hello')
// }

// // 不写返回值类型
// function hello2(txt: string) {
//   console.log('function hello2')
// }

// // 变量被赋值为一个函数
// // 一
// const n1 = function (txt: string) {
//   console.log('hello' + txt)
// }

// // 二
// const n2: (txt: string) => void
//   = function (txt) {
//     console.log('hello2' + txt)
//   }

// // 函数类型中的参数名和实际参数名可以不同
// let f: (x: string) => number;

// f = function (str: string) {
//   return 1
// }

// // 函数类型很长，使用type为函数类型定义一个别名
// type MyFunc = (txt: string) => void;
// const func: MyFunc = function (txt) {
//   console.log('自定义类型函数')
// }

// // 实际参数个数可以少于类型参数数量
// let myFunc: (a: number, b: number) => number;

// myFunc = (a: number) => a;

// // myFunc = (a: number, b: number, c: number) => a + b + c; // 报错


// function add(x: number, y: number) {
//   return x + y;
// }

// const myAdd: typeof add = function (x, y) {
//   return x + y;
// }


// 箭头函数
const repeat = (
  str: string,
  times: number
): string => str.repeat(times);


// 类型写在箭头函数定义里边
function greet(
  fn: (a: string) => void
): void {
  fn('world')
}