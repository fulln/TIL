---
dg-home: true
dg-publish: true
---
# life's a struggle 

> [!Abstract] 日拱一卒 
> 

```dataviewjs     
  
// 得到从当前开始前6个月份的yyyy-mm 数组

var m = Array(6).fill(0)
    .map(function(v,i){return i})
    .map(p=>new Date(new Date().setMonth(new Date().getMonth()-p))
    .toISOString().slice(0,7));

let codes = getCountMaps('code').reverse();
let leetcode = getCountMaps('leetcode').reverse();
let libs = getCountMaps('lib').reverse();
let dailys = getCountMaps('daily').reverse();
let wereads = getCountMaps('weread').reverse();

dv.header(4, "近半年文章统计");
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

总共有 **68** 篇微信读书
总共有 **74** 篇code文章
总共有 **155** 篇日常
总共有 **134** 篇学习文章
总共有 **592** 篇leetcode
 
总文章 ***1023*** 篇
