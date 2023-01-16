let today = moment().format("YYYY-MM-DD")

function todayWrite(){
    let li = app.fileManager.vault.fileMap
    let fileList = []
    getChildren(li["code"].children,fileList)

    console.log(fileList)

    fileList = fileList.map(f =>{
        return "- [["+f.name+"]] \n"
    })

    return fileList.join("")
}



function getChildren(list,fileList){
   list.forEach(e => {
       if (e.children) {
           getChildren(e.children,fileList)
       }else{
            let curr = moment(e.stat.ctime).format("YYYY-MM-DD")
		    if( curr == today){
			    fileList.push(e)
		    }
       }
   })
}

module.exports = todayWrite;