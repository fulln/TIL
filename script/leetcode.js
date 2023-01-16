async function leetcode() {

    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    var result = ""

    await fetch("http://raw.githubusercontent.com/fulln/TIL/master/menu.json", requestOptions)
        .then(response => response.json())
        .then(resp => {            
            let list = resp.top
            let date = new Date()
            let todayTime = date.toISOString().split('T')[0]
            // console.log("today is" + todayTime)    
            list.map(e => {
                if (e.indexOf(todayTime) != -1) {                    
                    result += e +"\n"                    
                }
            })            
        })
        .catch(error => console.log('error', error));
    
    // console.log("current log is" + result)    

    return result;
}

module.exports = leetcode;