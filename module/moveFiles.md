<%*

let li = app.fileManager.vault.fileMap
let fileList = []

getChildren(li["newFiles"].children,fileList)

function getChildren(list,fileList){  
   list.forEach(e => {  
       if (e.children) {  
           getChildren(e.children,fileList)  
       }else{       
			fileList.push(e)
       }  
   })  
}
fileList = fileList.map(f => {
	app.vault.adapter.remove(p)
})
%>