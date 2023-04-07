<%*
let li = app.fileManager.vault.fileMap

var s1 = getChildrenSize(li["weread"].children)
var s2 = getChildrenSize(li["code"].children)
var s3 = getChildrenSize( li["daily"].children)
var s4 = getChildrenSize( li["lib"].children)
var s5 = getChildrenSize( li["leetcode"].children)
let ret = ""
ret += `总共有 **${s1}** 篇微信读书\r\n` 
ret += `总共有 **${s2}** 篇技术总结文章\r\n`
ret += `总共有 **${s3}** 篇日常\r\n`
ret += `总共有 **${s4}** 篇学习文章\r\n`
ret += `总共有 **${s5}** 篇leetcode\r\n`
ret += ` \r\n`
ret += `总文章 ***${s5+s4+s3+s2+s1}*** 篇`

function getChildrenSize(list){  
   let	number = 0
   list.forEach(e => {  
       if (e.children) {  
           number += getChildrenSize(e.children,number)  
       }else{       
			number++
       }  
   }) 
   return number 
}
return ret
%>
