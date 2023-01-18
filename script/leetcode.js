async function leetcode() {

    // var requestOptions = {
    //     method: 'GET',
    //     redirect: 'follow'
    // };

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Cookie", "csrftoken=XHrPuYchOQACr4KjcVJqfMBjjwAcgbsLCT3EvKV1qQTw3M4n9jh3ihtxSCMvHDYK");

    var raw = JSON.stringify({
    "query": "\n    query recentAcSubmissions($username: String!, $limit: Int!) {\n  recentAcSubmissionList(username: $username, limit: $limit) {\n    id\n    title\n    titleSlug\n    timestamp\n  }\n}\n    ",
    "variables": {
    "username": "fulln",
    "limit": 15
    }
    });

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

// var result = ""

await fetch("https://leetcode.com/graphql/noj-go/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

    

    // await fetch("http://raw.githubusercontent.com/fulln/TIL/master/menu.json", requestOptions)
    //     .then(response => response.json())
    //     .then(resp => {            
    //         let list = resp.top
    //         let date = new Date()
    //         let todayTime = date.toISOString().split('T')[0]
    //         // console.log("today is" + todayTime)    
    //         list.map(e => {
    //             if (e.indexOf(todayTime) != -1) {                    
    //                 result += e +"\n"                    
    //             }
    //         })            
    //     })
    //     .catch(error => console.log('error', error));
    
    // // console.log("current log is" + result)    

    // return result;
}

module.exports = leetcode;