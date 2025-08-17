// let name: string;
function add(a, b) {
    return a + b;
}
// 函数返回的是一个number，所以可以完成赋值
var num = add(1, 2);
// TS中可以进行使用F2进行快速重命名
var haha = "kevin";
var phone = "1710099992830";
var x;
x = 1;
x = 'string';
x = true;
function add1(x, y) {
    return x + y;
}
add1(1, [2, 3]);
var x1 = "hello";
var y;
y = x1;
y * 123;
y.toFixed();
var x2;
x2 = true;
x2 = 123;
x2 = "hello";
// 报错：不能赋值给其他的变量，除了any和unknown
var v = 123;
// let v1: boolean = v;
// let v2: number = v;
// 报错： 不能直接调用unknown的方法和属性
var n1 = { foo: 123 };
// n.foo; // 报错
var n2 = 'heool';
// n2.trim(); // 报错
var n3 = function (n) {
    if (n === void 0) { n = 0; }
    return n + 1;
};
// n3(); // 报错
// never
function fn(x) {
    if (typeof x === 'string') {
        // ....
    }
    else if (typeof x === 'number') {
        // ....
    }
    else {
        x; // never类型
    }
}
function f() {
    throw new Error('error');
}
var f1 = f();
var f2 = f();
var f3 = f();
var arr = [1, 2, 3];
arr = [];
arr = [4, 4, 4, 4];
// 使用Array接口创建数组
var array;
array = [1, 2, 3, '4'];
var foo = arr[3];
console.log(foo);
