#obsidian 

使用这样的符号就可以启用callout模块: `> [!INFO]`.

```text
> [!INFO]
> 这里是callout模块
> 支持**markdown** 和 [[Internal link|wikilinks]].
```

呈现出来是这样的

> [!INFO]
> 这里是callout模块
> 支持**markdown** 和 [[Internal link|wikilinks]].

## 样式

默认有12种风格。每一种有不同的颜色和图标。

只要把上面例子里的 `INFO` 替换为下面任意一个就行。

-   note
-   abstract, summary, tldr
-   info, todo
-   tip, hint, important
-   success, check, done
-   question, help, faq
-   warning, caution, attention
-   failure, fail, missing
-   danger, error
-   bug
-   example
-   quote, cite

## 标题和内容

可以自定义标题，然后直接不要主体部分，比如

```text
> [!TIP] Callouts can have custom titles, which also supports **markdown**!
```

> [!TIP] Callouts can have custom titles, which also supports **markdown**!

## 折叠

可以使用 `+` 默认展开或者 `-` 默认折叠正文部分。

```text
> [!FAQ]- Are callouts foldable?
> Yes! In a foldable callout, the contents are hidden until it is expanded.
```

显示为:

> [!FAQ]- Are callouts foldable?
> Yes! In a foldable callout, the contents are hidden until it is expanded.


## 如果需要自定义

Callout的类型和图标是用CSS来描述，颜色是`r, g, b` 三色组，图标有相应的 icon ID (比如`lucide-info`)。也可以自定义SVG图标。

```css
.callout[data-callout="my-callout-type"] {
    --callout-color: 0, 0, 0;
    --callout-icon: icon-id;
    --callout-icon: '<svg>...custom svg...</svg>';
}
```