# CSS3手册

## 布局

![image-20250604224356739](images/CSS3手册/image-20250604224356739.png)

**浮动**：做文字环绕效果

**弹性盒**：单行或单列布局

**网格**：多行多列布局

### 弹性盒

#### 生成弹性容器和弹性项目

![image-20250604224919306](images/CSS3手册/image-20250604224919306.png)

默认情况下，弹性项目沿着主轴一次排列，侧轴拉伸

#### 更改方向

通过`flex-direction`可以更改主轴方向

![image-20250604225528777](images/CSS3手册/image-20250604225528777.png)

#### 主轴排列

通过`justify-content`属性，可以影响主轴的排列方式

![image-20250604225647403](images/CSS3手册/image-20250604225647403.png)

#### 侧轴排列

通过`align-items`属性，可以影响侧轴的排列方式

![image-20250604225814769](images/CSS3手册/image-20250604225814769.png)

#### 弹性项目伸缩

伸缩，指的是在主轴方向上，当弹性容器有额外空间时，是否需要拉伸，当空间不足时，是否需要压缩

在**弹性项目**上使用`flex`属性，可设置拉伸和压缩比例，`flex: 拉伸比例  压缩比例  初始尺寸`

拉伸实例：

![image-20250604230052391](images/CSS3手册/image-20250604230052391.png)

压缩实例：

![image-20250604230249251](images/CSS3手册/image-20250604230249251.png)

默认情况下，`flex: 0 1 auto`

#### 主轴换行

默认情况下，当主轴剩余空间不足时，按照压缩比例进行压缩，但如果设置了主轴换行，则不会进行压缩，直接换行显示

给弹性容器设置`flex-wrap: wrap`，即可实现主轴换行

![image-20250604230607916](images/CSS3手册/image-20250604230607916.png)

> 尽管主轴换行可以实现多行多列，但是真正的多行多列还是推荐网格布局。

### 网格

**网格布局是多行多列布局的最终解决方案**

#### 生成网格布局

![image-20250605002224495](images/CSS3手册/image-20250605002224495.png)

容器生成网格布局之后，所有的子元素为网格项目

#### 定义行和列

`grid-template-rows`：定义行

`grid-template-columns`：定义列

![image-20250605002758798](images/CSS3手册/image-20250605002758798.png)

#### 改变排列方向

使用属性`grid-auto-flow: column`，可使子元素按列排列

![image-20250605003050782](images/CSS3手册/image-20250605003050782.png)

#### 单元格之间的间隙

```css
row-gap: 10px;/* 行间距是10px */
column-gap: 20px; /* 列间距是20px */
gap: 10px 20px; /* 行间隙是10px， 列间隙是20px */
```

![image-20250605004006509](images/CSS3手册/image-20250605004006509.png)

#### 单元格内部的对齐

默认情况下，网格项目在单元格内部水平和垂直拉伸，以撑满单元格

可以使用`justify-items`设置水平方向的排列

可以使用`align-items`设置垂直方向排列方式

他们的可取值是相同的

```css
justify-items: start 左 | end 右 | center 中 | stretch 拉伸
align-items: start 上 | end 下 | center 中 | stretch 拉伸
```

![image-20250605004504512](images/CSS3手册/image-20250605004504512.png)

可以使用速写属性`place-items: 垂直对齐方式 水平对齐方式`同时设置这两个值

```css
place-items: start center /* 垂直靠上 水平居中 */
```

#### 网格项目定位

默认情况下，网格项目一次排列到单元格中，每个网格占据一个单元格

但是可以对网格设置`grid-area`属性来改变这一行为

使用方式为：

```css
grid-area: 起始行线编号/起始列线编号/结束行线编号/结束列线编号;
```

![image-20250605004955157](images/CSS3手册/image-20250605004955157.png)

## 视觉

> 视觉类样式，指的是不影响盒子位置、尺寸的样式，例如文字颜色、背景颜色、背景图片等

### 阴影

#### 盒子阴影

通过`box-shadow`属性可以设置整个盒子的阴影。

如下是一些实例：

![image-20250530004534843](images/CSS3手册/image-20250530004534843.png)

#### 文字阴影

通过`text-shadow`设置文字阴影。

以下是我们的实例：

![image-20250530004848671](images/CSS3手册/image-20250530004848671.png)

### 圆角

通过设置`border-radius`，设置盒子的圆角。

![image-20250530004947721](images/CSS3手册/image-20250530004947721.png)

`border-radius`可以有很多灵活的用法：比如以下代码：

```css
border-radius: 10px; /* 同时设置4个角的圆角，半径是10px */
border-radius: 50%; /* 同时设置四个角的圆角，圆的横向半径是宽度一半，纵向半径是高度一半 */
border-radius: 10px 20px 30px 40px; /* 分别设置左上、右上、右下、左下的圆角 */
```

![image-20250530005431860](images/CSS3手册/image-20250530005431860.png)

### 背景渐变

在设置背景图片时，除了可以使用`url()`加载一张背景图，还可以使用`linear-gradient()`函数来设置背景渐变。

`linear-gradient`用来创建一张渐变的图片，语法是：

```css
/* 设置渐变背景，方向：从上到下，颜色：从#e66465到#9198e5 */
background: linear-gradient(to bottom, #e66465, #9198e5);
```

![image-20250530005837506](images/CSS3手册/image-20250530005837506.png)

### 变形

通过`transform`属性，可以使得盒子的形态发生变化

该属性支持多种变形方案，常见的有：

- translate，平移
- scale，缩放
- rotate，旋转

无论是哪种**transform**，都只是视觉效果的变化，不会影响到盒子的布局。

`transform`不会导致浏览器reflow和rerender，因此效率很高。

#### translate平移

使用`translate`可以让盒子在原来的位置上产生位移，类似于相对定位。

![image-20250530010447399](images/CSS3手册/image-20250530010447399.png)

#### scale缩放

使用`scale`可以让盒子在基于原来的尺寸发生缩放。

![image-20250530010540238](images/CSS3手册/image-20250530010540238.png)

#### rotate旋转

使用`rotate`属性可以在原图的基础上进行旋转。

```css
/* 在原图的基础上，顺时针旋转45度 */
translate: rotate(45deg);
/* 在原图的基础上，顺时针旋转半圈 */
translate: rotate(0.5urn);
```

#### 改变变形圆点

变形圆点的位置，会影响到具体的变形行为

默认情况下，变形的圆点在盒子中心，你可以通过`transform-origin`来改变它。

```css
transform-origin: center; /* 设置圆点在盒子中心 */
transform-origin: left top; /* 设置原点在盒子左上角 */
transform-origin: right bottom; /* 设置圆点在盒子的右下角 */
transform-origin: 30px 60px; /* 设置圆点在盒子坐标的(30, 60)位置 */
```

## 过渡和动画

使用过渡与动画，可以使得CSS属性变得更加丝滑

**过度与动画无法对所有的CSS属性产生影响，能够产生影响的只有数值类属性**，比如宽高、颜色、字体大小等等

### 过渡

```css
transition: 过渡属性  持续时间  过度函数  过度延迟
```

- 过渡属性

​	针对哪一个CSS属性应用过渡。例如填写`transform`，表示仅仅针对**transform**属性使用过渡。如果填写`all`或者不填写，默认是应用于所有的CSS属性。

- 持续时间

​	CSS属性变化所持续的时间，需要带上单位，`3s`表示3秒，`0.5s`或`500ms`表示500毫秒

- 过度函数

​	本质上是CSS属性变化的贝塞尔曲线函数，通常是直接使用预设值：

​	`ease-in-out`：平滑开始，平滑结束。

​	`linear`：线性变化。

​	`ease-in`：仅仅是平滑开始。

​	`ease-out`：仅平滑结束。

- 过渡延迟

​	书写规则和持续时间一样，表示过渡效果延迟多久之后触发，不填没有延迟

**在JS中，可以监听元素的`transitionstart`和`transitionend`事件，从而在过渡开始和过渡结束做一些别的事情。**

### 动画

动画的本质就是预先定义一套CSS变化规则，然后给这个规则起名字

![image-20250604000434028](images/CSS3手册/image-20250604000434028.png)

之后，其他元素就可以使用这个规则：

```css
animation: 规则名  持续时间;
```

在应用规则时，还可以指定更多的信息

```css
animation: 规则名  持续时间  重复次数  时间函数  动画方向  延迟时间
```

> 细节：
>
> - 定义规则时，`0%`可以写成`from`
> - 定义规则时，`100%`可以写成`to`
> - 重复次数为`infinite`时，表示无限重复
> - 动画方向为`alternate`时，表示交替方向，第一次正向，第二次反向，第三次正向，第四次反向，以此类推

## 其他

### box-sizing

![image-20250605225547440](images/CSS3手册/image-20250605225547440.png)

> 原本的设置宽高是在内容身上设置的，可见区域其实是要大于内容区域的，导致实际的值可能不只有100px，使用box-sizing: border-box;可以设置成边框的宽高是100px。

使用`border-box`控制尺寸更加直观，因此很多网站都会加上如下代码：

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
```

### 图像内容适应

CSS3属性`object-fit`可以控制**多媒体内容和元素**的适应方式。通常适用于`img`或者`video`元素中。

下图中所有的`img`元素均被固定了宽高，溢出img的部分实际上不会显示。

![image-20250605230127962](images/CSS3手册/image-20250605230127962.png)

### 视口单位

视口单位有两个：`vw` 和 `vh`，对应的是`viewport width`和 `viewport height`分别用来设置视口的宽度和高度

`1vw`就是视口的1%，`100vw`就是视口的100%

### 伪元素选择器

通过`::before`和`::after`选择器，可以通过CSS给元素生成两个子元素。

![image-20250605230907588](images/CSS3手册/image-20250605230907588.png)

使用伪元素可以避免在代码中使用过多的空元素

**伪元素必须要有content属性，否则不会生效，如果不需要有内容，设置`content: ''`即可**

### 平滑滚动

> 参考MDN：https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-behavior

使用`scroll-behavior: smooth`，可以让滚动更加丝滑

### 字体图标

CSS3新增了`font-face`指令，该指令可以让我们加载网络字体

```css
h1 {
  font-family: 翩翩体-简
}

@font-face {
  font-family: 翩翩体-简;
  src: url(字体的加载路径)
}
```

最常见的使用方式就是字体图标

**字体图标的本质上是文字，通过font-size设置大小，color设置颜色**

国内使用最多的就是阿里巴巴的矢量图标库:https://www.iconfont.cn/













