let arr: number[] = [1, 2, 3];

arr = []
arr = [4, 4, 4, 4];

// 使用Array接口创建数组
let array: Array<number | string>;
array = [1, 2, 3, '4'];

let foo = arr[3];

// 读取数组成员
type Names = string[];
type Name = Names[0]; // string



// 只读数组
const readonlyArr: readonly number[] = [1, 2, 3];
readonlyArr[1] = 2;// 报错
readonlyArr.push(4); // 报错
delete readonlyArr[0]; // 报错