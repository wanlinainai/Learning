// let x: any

// x = 1
// x = 'string'
// x = true

// function add1(x, y) {
//   return x + y;
// }

// add1(1, [2, 3])



// let x1: any = "hello"
// let y: number;

// y = x1;

// y * 123;
// y.toFixed();


// let x2: unknown;

// x2 = true;
// x2 = 123;
// x2 = "hello";


// // 报错：不能赋值给其他的变量，除了any和unknown
// let v: unknown = 123;
// // let v1: boolean = v;
// // let v2: number = v;

// // 报错： 不能直接调用unknown的方法和属性
// let n1: unknown = { foo: 123 };
// // n.foo; // 报错

// let n2: unknown = 'heool';
// // n2.trim(); // 报错

// let n3: unknown = (n = 0) => n + 1;
// // n3(); // 报错



// // never
// function fn(x: string | number) {
//   if (typeof x === 'string') {
//     // ....
//   } else if (typeof x === 'number') {
//     // ....
//   } else {
//     x; // never类型
//   }
// }

// function f(): never {
//   throw new Error('error');
// }

// let f1: number = f();
// let f2: string = f();
// let f3: boolean = f();