
// 元组
// const s: [string, number, boolean] = ['a', 1, true]

// // 数组
// const arr: number[] = [1]
// // 元组
// const tuple: [number] = [1]

// // let a: [number, string?, number]

// let x: [string, string] = ['a', 'b'];

// // x[2] = 'c' // 报错

// type NamedNums = [
//   string,
//   ...number[]
// ];

// const a: NamedNums = ['a', 1, 2, 3]
// const b: NamedNums = ['b', 1];


// // 只读yuanzu 
// type t = readonly [number, number];

// // 写法二
// // type t2 = Readonly<[number, number]>


// 父子类型
// type t1 = readonly[number, string]
// type t2 = [number, string]

// let x: t2 = [1, 'a']
// let y: t1 = x;

// x = y;


