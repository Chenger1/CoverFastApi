function send_request(data, url){
    let xhr = new XMLHttpRequest();

    xhr.open('POST', url);
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');  // set header to JSON instead of Form Data
    xhr.send([data]);

    xhr.onreadystatechange = function(){
        if (xhr.readyState !=4) return;

        console.log(JSON.parse(xhr.response));
        let response = JSON.parse(xhr.response);
        if(response){
            alert('Success');
        }else{
            alert('Error');
        }
    }
}
