---
dg-publish: true
---
```dataviewjs

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