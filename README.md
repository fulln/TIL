---
dg-home: true
dg-publish: true
---
# About me

## 三观

**人生观**: 不喜欢束缚，不喜欢形式主义，不喜欢重复，不喜欢既定的人生（什么时间该做什么事情），这样会和当下社会观念背向而驰，但还是向往自由。

**价值观**: 一个字就是卷，就像踩单车一样，可以在任何时候停止踩单车。有些车道你参加卷的资格都没有。原生的家庭并不会让我处于一个很好的赛道，但是我仍然在路上。

**世界观**: 全世界都是草台班子，整个社会都是顺从性实验的结果，世界的运行法则针对不同的人群是有不同的规则的。道德的约束只能在同一个人群生效，约束不了另外一个人群，对于人来说，是有多套人群标签的。

> [!note] 2023 tags
> #日漫 #程序员 #散漫 #随和 #科技爱好者 #探索   #系统设计 #java #python  #规划者

# life's a struggle 

> [!Abstract] 日拱一卒 
> 

```dataviewjs     
  
// 得到从当前开始前6个月份的yyyy-mm 数组

var m = Array(12).fill(0)
    .map(function(v,i){return i})
    .map(p=>new Date(new Date().setMonth(new Date().getMonth()-p))
    .toISOString().slice(0,7));

let codes = getCountMaps('code').reverse();
let leetcode = getCountMaps('leetcode').reverse();
let libs = getCountMaps('lib').reverse();
let dailys = getCountMaps('daily').reverse();
let wereads = getCountMaps('weread').reverse();

dv.header(4, "每月文章统计");
dv.paragraph(`\`\`\`chart
type: line
labels: [${m.reverse()}]
labelColors: true
series:
- title: code总结文章
  data: [${codes}]
- title: lib学习文章
  data: [${libs}]
- title: 日常总结文章
  data: [${dailys}]
- title: 读书笔记
  data: [${wereads}]
- title: leetcode
  data: [${leetcode}]
\`\`\``)


function getCountMaps(name) {
    let codeDataMap = new Map();
    // 转成map
    const codeMaps = dv.pages(`"${name}"`)
        .groupBy(p => String(p.file.cday).slice(0, 7))
    init:   
    for (let i of m) {
        for (let ele of codeMaps) {
            if(ele.key === i){
                 codeDataMap.set(i, ele.rows.length);
                 continue init
            }
        }
        codeDataMap.set(i, 0);
    }
    // 返回 array 数组
    return Array.from(codeDataMap.values());

}

```

总共有 **80** 篇微信读书
总共有 **90** 篇code文章
总共有 **253** 篇日常
总共有 **261** 篇学习文章
总共有 **601** 篇leetcode
 
总文章 ***1285*** 篇