---
dg-publish: true
---
```dataviewjs

var i = [dv.pages(`"weread"`).length] 
dv.paragraph(`总共有 **${i[0]}** 篇微信阅读`)  

dv.list(dv.pages(`"weread"`)
	.filter(p=>{
		if(p.file.name == 'readme'){
			return false
		}else{
			return true
		}
	})
	.sort(p=>p.lastReadDate,'desc')
	.map(p=>moment(Number(p.lastReadDate)).format('yyyy-MM-DD') +' >> '+ p.file.link)) 


```