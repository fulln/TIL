<%*

let li = app.fileManager.vault.fileMap
let fileList = []
let checkDate = tp.file.creation_date("YYYY-MM-DD")

getChildren(li["leetcode"].children,fileList)

function getChildren(list,fileList){  
   list.forEach(e => {  
       if (e.children) {  
           getChildren(e.children,fileList)  
       }else{       
		    if(moment(e.stat.ctime).format("YYYY-MM-DD") == checkDate){
		
			    console.log(e)
			    fileList.push(e)
		    }
       }  
   })  
}

fileList = fileList.map(f => {
    return "- [["+f.name+"]]\n"
})

return fileList.join("")


%>