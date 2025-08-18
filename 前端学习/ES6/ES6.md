# ES 6

## 简介

### Babel转码器

Babel是一个广泛使用的ES6转码器，可以将ES6转成ES5代码。

```javascript
input.map(item => item + 1);

// 转码后
input.map(function (item) {
    return item + 1;
})
```

项目中安装Babel。

```shell
npm install --save-dev @babel/core
```

#### 配置文件 `.babelrc`

`.babelrc`是Babel配置文件，存放在项目的跟路径中。

该文件用来设置转码规则和插件。

```json
{
    "presets": [],
    "plugins": []
}
```

`presets`设置转码规则，官方提供以下的规则集。

```shell
npm install --save-dev @babel/preset-env # 最新转码规则

npm install --save-dev @babel/preset-react # React转码规则
```

```json
 {
    "presets": [
      "@babel/env",
      "@babel/preset-react"
    ],
    "plugins": []
  }
```

以下所有Babel工具的使用，必须写好`.babelrc`。

#### 命令行转码

Babel提供命令行工具`@babel/cli`，用于命令行转码。

安装如下：

```shell
npm install --save-dev @babel/cli
```

基本用法：

```shell
# 转码结果输出到标准输出
$ npx babel example.js

# 转码结果写入一个文件
# --out-file 或 -o 参数指定输出文件
$ npx babel example.js --out-file compiled.js
# 或者
$ npx babel example.js -o compiled.js

# 整个目录转码
# --out-dir 或 -d 参数指定输出目录
$ npx babel src --out-dir lib
# 或者
$ npx babel src -d lib

# -s 参数生成source map文件
$ npx babel src -d lib -s
```

