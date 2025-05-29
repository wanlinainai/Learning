# CSS3手册

## 布局





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























