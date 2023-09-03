<%*
let recent  = app.workspace.getRecentFiles()
let tops = []

recent.forEach(e =>{
	let tfile = tp.file.find_tfile(e)
	if(tfile){
		let currDates = new Date(tfile.stat.mtime).toLocaleString()
		let httpulrs =  "https://github.com/fulln/TIL/blob/master/" + tfile.path
		tops.push("* ["+tfile.basename+"]("+encodeURI(httpulrs)+") - "+currDates)
	}
})
const fs = require('fs');
let upadtePath = app.vault.adapter.basePath +'/menu.json'
fs.readFile(upadtePath, 'utf8', (err, data) => {
    if (err) throw err;
    let menu = JSON.parse(data);
    menu.top = tops
    fs.writeFile(upadtePath, JSON.stringify(menu), (err) => {
        if (err) throw err;
        console.log('It\'s saved!');
    });
})
%>
