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