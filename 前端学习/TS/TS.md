# TS

## TS中的接口和类型兼容性

> 扩展类型- 接口
>
> 扩展类型：类型别名、枚举、接口、类

## 基本类型约束

### 如何进行类型约束？

变量、函数参数、函数返回值。`xxx:Type`

TS在很多场景可以进行类型推导。

`any`：表示任意类型，对该类型TS不进行类型检查。

### 动态类型和静态类型

JavaScript的类型限制非常弱，比如下面的JavaScript代码：

```javascript
// 一
let x = 1;
x = "Heool";

// 二
let y = { foo: 1 };
delete y.foo;
y.bar = 2;
```

上述的代码中，变量`x`声明时，值的类型就是`number`类型，但是可以改成`string`。不能提前知道类型是什么。

`TypeScript`引入了一个更加强大的类型系统，属于静态类型语言。

还是之前的代码示例，在赋值的时候，typescript就已经确定了类型，之后不允许在修改类型。即变量是静态的。

> Typescript必须需要赋值之后才可以使用，否则报错。
>
> ```typescript
> let x:number;
> console.log(x);// 报错
> ```

### tsc 命令

1. --outFile

如果将多个TS文件编译成JS。

```shell
tsc file1.ts file2.tx --outFile app.js
```

2. --outDir

指定到其他目录

```shell
tsc app.ts --outDir dist
```

3. --target

指定编译的版本。tsc默认会将TS代码编译成很低的ES版本（3.0）

```shell
tsc --target es2025 app.ts
```

### tsconfig.json

TS允许将`tsc`编译参数写在`tsconfig.json`中。

```
tsc file1.ts file2.ts --outFile dist/app.js
```

转成json就是

```json
{
  "files": ["file1.ts", "file2.ts"],
  "compilerOptions": {
    "outFile": "dist/app.js"
  }
}
```

有了这个文件，直接调用tsc即可。

## any类型，unknown类型，never类型

any类型就是TS不对该变量或方法进行类型检查。

```typescript
let x: any

x = 1
x = 'string'
x = true

function add1(x, y) {
  return x + y;
}

add1(1, [2, 3])
```

> typescript提供了一个编译选项`noImplicitAny`。打开这个选项，只要判断是any就报错。
>
> ```shell
> tsc --noImplicitAny app.ts
> ```
>
> 有一个特殊情况，即使打开了这个选项，使用`let`和`var`命令声明变量，不赋值不指定特定类型，不报错。
>
> ```typescript
> var x;
> let y;
> ```

any 会“污染”其他变量，他可以赋值给其他任何类型的变量，导致其他变量出错。

```typescript

let x1: any = "hello"
let y: number;

y = x1;

y * 123;
y.toFixed();
```

上述代码都不会报错，我们将string类型的x1赋值给y，y进行对应的操作，TS也不会报错，只有到了运行的时候才会报错。这也是不建议使用any的原因。

### unknown类型

其实就是严格版的any。

```typescript
let x2: unknown;

x2 = true;
x2 = 123;
x2 = "hello";


// 报错：不能赋值给其他的变量，除了any和unknown
let v: unknown = 123;
let v1: boolean = v;
let v2: number = v;

// 报错： 不能直接调用unknown的方法和属性
let n1: unknown = { foo: 123 };
n.foo; // 报错

let n2: unknown = 'heool';
n2.trim(); // 报错

let n3: unknown = (n = 0) => n + 1;
n3(); // 报错
```

`unknown`类型的变量能够进行运算是有限的，只能进行比较运算（`==`，`===`，`!=`，`!==`，`||`，`&&`， `?`）、取反运算（运算符`!`）、`typeof`运算和`instanceof`运算符。

> 怎么使用这个变量呢？
>
> 缩小unknown变量的类型范围，确保不会出错。
>
> ```typescript
> let a:unknown = 1;
> 
> if(typeof a === 'number') {
>   let r = a + 10;
> }
> ```
>
> 这样设计的原因是只有明确unknown变量的实际类型，才能使用它。防止像any一样滥用，“污染”其他变量。

### never类型

为了保持与集合论的对应关系，以及类型运算的完整性，引入了空类型的概念。

```typescript
let x: never
```

变量x类型是never，不可能赋值任何值，否则报错。

```typescript
// never
function fn(x: string | number) {
  if (typeof x === 'string') {
    // ....
  } else if (typeof x === 'number') {
    // ....
  } else {
    x; // never类型
  }
}
```

如果一个变量可能是多种类型，通常需要使用分支处理每一种类型，这时，如果处理完所有的类型之后，剩下的就是`never`类型。

`never`一个重要特点是，可以赋值给任意其他类型：

```typescript
function f(): never {
  throw new Error('error');
}

let f1: number = f();
let f2: string = f();
let f3: boolean = f();
```

上述示例中，函数f()会抛出错误。

为什么never可以赋值给其他类型呢？和集合论有关，空集是任何集合的子集，Typescript就规定了，任何类型都包含了`never`类型。

## 数组

根本特征：所有的成员类型必须相同，但是成员数量是不固定的。

数组类型的定义有两种方式：第一种在类型后加上[]。

```typescript
let arr: number[] = [1,2,3];
```

```typescript
let arr: (number | string)[];
```

第二种是利用Array接口。

```typescript
let arr: Array<number> = [1,2,3]
```

```typescript
let arr: Array<number | string>;
```

上述写法属于泛型。

由于数组成员是可以动态变化的，所以TS并不会对数组边界进行检查，越界访问不会报错。

```typescript
let arr: number[] = [1,2,3]
let foo = arr[3]; // 正确
```

上述示例中，变量`foo`的值是一个不存在的 数组成员，TS不会报错。

TS允许使用方括号读取数组成员类型。

```typescript
type Names = string[];
type Name = Names[0]; // string
```

Names是string数组，那么Name就是string类型。

```typescript
type Names = string[];
type Name = Names[number];
```

上述表示数组Names所有数值索引成员类型，返回的是string.

### 数组类型判断

如果数组类型没有声明，TS会推断数组成员的类型，此时，推断行为会因为值的不同，而有所不同。

如果数组初始化是空数组，那么TS判断数组类型是any[]。

```typescript
const arr = []; // 推断是any[]
```

之后赋值的时候，TS会自动更新类型判断。

```typescript
const arr = [];
arr; // any[]类型

arr.push(1);
arr // number类型

arr.push('hello');
arr // number | string类型
```

### 只读数组，const 断言

TS允许声明只读数组，方法是在数组类型之前加上`readonly`关键字。

```typescript
const readonlyArr: readonly number[] = [1, 2, 3];
readonlyArr[1] = 2;// 报错
readonlyArr.push(4); // 报错
delete readonlyArr[0]; // 报错
```

上述数组内容增加、修改、删除都会报错。

TS中的只读数组和数组视为两种类型，后者是前者的子类型。

只读数组中没有push、pop之类的改变数组的方法，所以number[]的方法数量要多于readonly number[]。

TS提供了两个专门的泛型，用来生成只读数组的类型。

```typescript
const a1: ReadonlyArray<number> = [0, 1];
const a2: Readonly<number[]> = [0, 1];
```

还有一种声明只读数组的方法：

```typescript
const arr = [0, 1] as const 
arr[0] = [2]; // 报错；
```

### 多维数组

```typescript
let multi: number[][] = [[1,2,3], [4,5,6]]
```





















